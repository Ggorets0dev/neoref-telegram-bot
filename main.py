'''Telegram bot initialization'''

import asyncio
import os
import openai
from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.methods import DeleteWebhook

from models.gpt import ChatGpt
from models.query_queue import QueryQueue

from utils.config import Config

from handlers import start, add, helph, delh, queue, context, info, conversation


__VERSION__ = '1.0.0'


# NOTE - Change logger settings
logger.add('logs/bot.log', rotation='256 MB')


# SECTION - Checking config
CONFIG = None
CONFIG_PATH = 'config.yaml'

if os.path.isfile(CONFIG_PATH) and Config.get(CONFIG_PATH).get('admin_ids') is not None:
    Config.save_path(CONFIG_PATH)
    CONFIG = Config.get_saved()
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
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    logger.error('Key for accessing Telegram was not found in the environment variables')
    exit(1)

logger.info("Trying to access Telegram using provided bot token...")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logger.success('Logged in Telegram')
# !SECTION


# SECTION - Check OpenAI API
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
MAX_TOKENS = CONFIG.get('chat_max_tokens')
MODEL = CONFIG.get('chat_model')
CHECK_TIMOUT, ASK_TIMEOUT = CONFIG.get('chat_check_timeout'), CONFIG.get('chat_ask_timeout')
QUERY_LIMIT = CONFIG.get('query_max_count')

if not OPENAI_KEY:
    logger.error('Token for accessing OpenAI was not found in the environment variables')
    exit(1)
elif not MAX_TOKENS:
    logger.error('Tokens limit for ChatGPT was not found in the configuration file')
    exit(1)
elif not MODEL:
    logger.error('Model for ChatGPT was not found in the configuration file')
    exit(1)
elif not CHECK_TIMOUT or not ASK_TIMEOUT:
    logger.error('Maximum response time from ChatGPT is not defined in the configuration file')
    exit(1)
elif not CHECK_TIMOUT or not ASK_TIMEOUT:
    logger.error('Maximum response time from ChatGPT is not defined in the configuration file')
    exit(1)
elif not QUERY_LIMIT:
    logger.error('No limit on simultaneous requests detected in the configuration file')
    exit(1)

logger.info("Trying to access ChatGPT using provided API key...")

ChatGpt.set_api_key(OPENAI_KEY)
ChatGpt.set_max_tokens(int(MAX_TOKENS))
ChatGpt.set_model(MODEL)
ChatGpt.set_timeouts(CHECK_TIMOUT, ASK_TIMEOUT)
QueryQueue.set_query_limit(QUERY_LIMIT)

try:
    API_KEY_VALIDATION = ChatGpt.check_api_key(OPENAI_KEY, tries_cnt=5)

except openai.PermissionDeniedError:
    logger.error('Failed to connect to OpenAI server, permission denied')
    exit(1)

else:
    if API_KEY_VALIDATION:
        logger.success('OpenAI API key is valid, settings for ChatGPT are set')
    else:
        logger.error('OpenAI key is invalid')
        exit(1)
# !SECTION

async def main_polling():
    '''Entry point of the application'''
    logger.warning("Bot is running in polling mode, it is recommended to use webhooks for stable connection")
    dp.include_routers(start.router, helph.router, add.router, delh.router, context.router, queue.router, info.router, conversation.router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, fsm_strategy=FSMStrategy.USER_IN_CHAT)


if __name__ == '__main__':   
    asyncio.run(main_polling())
