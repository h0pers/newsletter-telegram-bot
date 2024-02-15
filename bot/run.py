import asyncio
import logging
import sys

from bot.main import start_bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
