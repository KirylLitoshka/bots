from aiohttp import web
from utils.ngrok import get_base_url
from utils.applications import init_bot_application
from config.tokens import BotTokens
from config.settings import WEBHOOK_PATH


async def on_startup(app: web.Application):
    app["base_url"] = get_base_url()


async def on_shutdown(app: web.Application):
    # Actions when app closing
    print(app['base_url'])


async def main_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    for bot in BotTokens:
        app.add_subapp(f'{WEBHOOK_PATH}/{bot.value}', init_bot_application(bot))
    return app
