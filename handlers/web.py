from aiogram import Bot, Dispatcher, types
from aiohttp import web


async def proceed_update(req: web.Request):
    updates = [types.Update(**(await req.json()))]
    Bot.set_current(req.app['dp'].bot)
    Dispatcher.set_current(req.app['dp'])
    await req.app['dp'].process_updates(updates)
    return web.Response()
