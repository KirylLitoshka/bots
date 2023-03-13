from aiohttp import web
from utils.ngrok import get_base_url


async def on_startup(app: web.Application):
    app["base_url"] = get_base_url()


async def on_shutdown(app: web.Application):
    # Actions when app closing
    print(app['base_url'])


async def main_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app
