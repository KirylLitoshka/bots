from aiohttp import web

from config import dispatchers, settings
from handlers.web import proceed_update


async def on_sub_startup(app):
    bot_name = app["bot_name"]
    bot_token = app["bot_token"]
    app['dp'] = await dispatchers.DISPATCHERS[bot_name](bot_token)
    url = f"{settings.BASE_URL}/tg/webhook/{app['bot_token']}/bot"
    await app['dp'].bot.set_webhook(url)


async def on_sub_shutdown(app):
    dp = app['dp']
    await dp.bot.delete_webhook()
    current_session = await dp.bot.get_session()
    if not current_session.closed:
        await current_session.close()
    if dp.storage is not None:
        await dp.storage.close()
        await dp.storage.wait_closed()


def init_bot_application(bot):
    app = web.Application()
    app["bot_token"] = bot.value
    app["bot_name"] = bot.name
    app.on_startup.append(on_sub_startup)
    app.on_shutdown.append(on_sub_shutdown)
    app.router.add_post("/bot", proceed_update)
    return app
