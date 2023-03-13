import os
import json
import aiofiles


def load_dialogs(path, filename):
    with open(f"{path}/{filename}.json", encoding="utf8") as fp:
        file_data = fp.read()
        return json.loads(file_data)


def load_users(storage_dir: str):
    users_data = {}
    users_storage = os.path.join(storage_dir, "users")
    if not os.path.exists(users_storage):
        os.makedirs(users_storage)
        return users_data
    *_, users_files = list(*os.walk(users_storage))
    if not users_files:
        return users_data
    for user_file_name in users_files:
        user_id = user_file_name.split(".")[0]
        with open(f"{users_storage}/{user_file_name}", encoding="utf8") as fp:
            file_data = json.loads(fp.read())
            users_data[user_id] = file_data
    return users_data


async def save_user(dispatcher, user_id, user):
    users_storage = os.path.join(dispatcher.data["dirs"]["STORAGE_DIR"], "users")
    async with aiofiles.open(f"{users_storage}/{user_id}.json", "w", encoding="utf8") as fb:
        await fb.write(json.dumps(user, indent=4, ensure_ascii=False))
