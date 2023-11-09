'''Telegram bot initialization'''

import asyncio
import os
from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from utils.config import Config

from handlers import start, add, helph


__VERSION__ = '0.3.0'


# NOTE - Change logger settings
logger.add('bot_logs.log', rotation='256 MB')

# SECTION - Loading config
CONFIG_PATH = 'config.yaml'

if os.path.isfile(CONFIG_PATH) or Config.get(CONFIG_PATH).get('admin_ids') is None:
    Config.save_path(CONFIG_PATH)
    logger.success('Path to the config saved')
else:
    logger.error('Config file was not detected or there are no ids of bot admins')
    exit(1)
# !SECTION


# SECTION - Loading .env
if os.path.isfile('.env'):
    load_dotenv('.env')
    logger.success('Environment file loaded')
else:
    logger.error('Environment file was not detected')
    exit(1)
#!SECTION


# SECTION - Sign in to Telegram
TOKEN = os.environ.get('TELEGRAM_TOKEN')

if not TOKEN:
    logger.error('Token for accessing Telegram was not found in the environment variables')
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logger.success('Logged in Telegram')
# !SECTION


async def main_polling():
    '''Entry point of the application'''
    logger.warning("Bot is running in polling mode, it is recommended to use webhooks for stable connection")
    dp.include_routers(start.router, helph.router, add.router)
    await dp.start_polling(bot, fsm_strategy=FSMStrategy.USER_IN_CHAT)


if __name__ == '__main__':   
    asyncio.run(main_polling())

# $argon2id$v=19$m=131072,t=10,p=4$h68ViZCap3xWIPpl7D7cMPjOHmrWRZpm+h29/aZ2Zpf4pmVJMBjf+ov1dIZaUoIvJbzlK7JyZC4/Q16uc6IkBAwqUpALySdBpaTtxeX+XoPZEQvMM2CZwkg0PdjB/Scd5IUSOox+0TL5xHTit6srpooBKAHiv52jX7Ni0yOwGTw$FnlMt+oU6Fvc5S3Zv9lS3d20NYygasWd74D8uWMviAHiagfPDULZpD0hyPdWRHTeSkyIqiRwbhrAXhv5BGCJ3roViUpSHjC9nt54qKMtloa4UKGMAN/iFK64x8o0eseZXWZ/Olb0WSPrWekj5nZs4XAKDhryKqJ8EuGIPByZdHY
