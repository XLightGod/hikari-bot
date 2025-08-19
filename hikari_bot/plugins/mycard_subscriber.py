import asyncio
import aiohttp
import json
from nonebot import get_driver, logger
from nonebot.adapters.onebot.v11 import Bot
from hikari_bot.utils.constants import *

_stop_event = asyncio.Event()

async def ws_runner():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(WS_URL, heartbeat=30) as ws:
                    logger.info("[mycard] 已连接到 WS")
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            try:
                                data = json.loads(msg.data)
                                logger.info(f"[mycard event] {data}")
                            except Exception:
                                logger.warning(f"[mycard raw] {msg.data}")
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            logger.warning("[mycard] 连接被关闭或出错，准备重连")
                            break
        except Exception as e:
            logger.error(f"[mycard] WS 出错：{e}")
        await asyncio.sleep(1)  # 出错/断开 → 1 秒后重连


driver = get_driver()
@driver.on_bot_connect
async def _on_bot_connect(bot: Bot):
    asyncio.create_task(ws_runner())