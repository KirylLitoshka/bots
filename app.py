import asyncio
import logging
import sys

from aiohttp import web
from config import settings

from base.app import main_app

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(main_app(), host=settings.APP_HOST, port=settings.APP_PORT)
