import asyncio

import aioschedule

from catalogues.appsell.handlers import send_messages_to_admin


async def test_task(dp):

    aioschedule.every(5).seconds.do(send_messages_to_admin, dp)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
