import os


from aiofiles import open
from aiogram import Dispatcher

__all__ = ["create_new_user"]


async def create_new_user(user_id):
    dp = Dispatcher.get_current()
    if user_id in dp.data['users']:
        return
    user = {

    }
    dp.data['users'][user_id] =



async def save_user():
    pass
