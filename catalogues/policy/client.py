import aiohttp
import shortuuid

from catalogues.policy.settings import SITE_DOMAIN, SITE_ID


async def create_new_version(endpoint, session):
    async with session.post(f"{endpoint}/v1beta1/sites/{SITE_ID}/versions") as resp:
        response_data = await resp.json()
        if response_data["status"] != "CREATED":
            raise
        response_site_version = response_data["name"].split("/")[-1]
        return response_site_version


async def get_uploaded_hashes(session, endpoint, version, file_hash, user_url):
    post_url = f"{endpoint}/v1beta1/sites/{SITE_ID}/versions/{version}:populateFiles"
    post_data = {"files": {f"/{user_url}": file_hash}}
    async with session.post(url=post_url, json=post_data) as resp:
        response_data = await resp.json()
        if response_data.get("error"):
            return None
        return response_data


async def upload_hashed_data(data, headers, gzip_file):
    async with aiohttp.ClientSession(headers=headers) as session:
        for upload_hash in data["uploadRequiredHashes"]:
            url = f"{data['uploadUrl']}/{upload_hash}"
            async with session.post(url, data=gzip_file) as response:
                if response.status != 200:
                    raise


async def update_version_status(endpoint, session, version):
    patch_url = f"{endpoint}/v1beta1/sites/{SITE_ID}/versions/{version}?update_mask=status"
    patch_data = {"status": "FINALIZED"}
    async with session.patch(url=patch_url, json=patch_data) as resp:
        response_data = await resp.json()
        if response_data.get("error"):
            raise


async def deploy_current_version(endpoint, session, version):
    deploy_url = f"{endpoint}/v1beta1/sites/{SITE_ID}/releases?versionName=sites/{SITE_ID}/versions/{version}"
    async with session.post(deploy_url) as response:
        if response.status != 200:
            raise


async def get_latest_version(session, endpoint):
    url = f"{endpoint}/v1beta1/sites/{SITE_ID}/versions"
    async with session.get(url) as resp:
        versions_list = await resp.json()
        if "versions" not in versions_list:
            return None
        finalized_versions_list = [version for version in versions_list["versions"] if version["status"] == "FINALIZED"]
        if not finalized_versions_list:
            return None
        return finalized_versions_list[0]["name"].split("/")[-1]


async def clone_version(session, endpoint, version):
    url = f'{endpoint}/v1beta1/sites/{SITE_ID}/versions:clone'
    post_data = {
        "sourceVersion": f"sites/{SITE_ID}/versions/{version}"
    }
    async with session.post(url, json=post_data) as response:
        response_data = await response.json()
        if response_data.get("error"):
            raise
        return response_data["name"]


async def get_operation_version(session, endpoint, operation_url):
    url = f"{endpoint}/v1beta1/{operation_url}"
    async with session.get(url) as response:
        response_data = await response.json()
        if response_data["done"]:
            full_version_name = response_data["response"]["name"]
            return full_version_name.split("/")[-1]
        else:
            raise


async def get_current_version(session, endpoint):
    latest_version = await get_latest_version(session, endpoint)
    if latest_version is None:
        return await create_new_version(endpoint, session)
    operation_url = await clone_version(session, endpoint, latest_version)
    version = await get_operation_version(session, endpoint, operation_url)
    return version


async def create_page(token, file_hash, gzip_file, user):
    headers = {"Authorization": "Bearer " + token}
    endpoint = "https://firebasehosting.googleapis.com"
    app_name = user["application_name"].replace(" ", "_").lower()
    user_url = f"{shortuuid.ShortUUID().random(length=10)}_{app_name}.html"
    async with aiohttp.ClientSession(headers=headers) as session:
        version = await get_current_version(session, endpoint)
        preloaded_data = await get_uploaded_hashes(session, endpoint, version, file_hash, user_url)
        if preloaded_data is None:
            raise
        await upload_hashed_data(preloaded_data, headers, gzip_file)
        await update_version_status(endpoint, session, version)
        await deploy_current_version(endpoint, session, version)
    return f"{SITE_DOMAIN}/{user_url}"
