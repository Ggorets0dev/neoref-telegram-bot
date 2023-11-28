'''Handlers for info command'''

from aiogram import Router, html
from aiogram.types import Message
from aiogram.filters import Command

from utils.config import Config

router = Router()

@router.message(Command("info"))
async def info_cmd(message: Message):
    '''Show bot information for user'''
    CONFIG = Config.get_saved()
    report = str()

    report += f"{html.bold('Модель ChatGPT:')} {CONFIG.get('chat_model')}\n\n"
    report += f"{html.bold('Лимит токенов:')} {CONFIG.get('chat_max_tokens')} шт.\n\n"
    report += f"{html.bold('Лимит активных запросов:')} {CONFIG.get('query_max_count')} шт.\n\n"
    report += f"{html.bold('Лимит ожидания ответа от модели:')} {CONFIG.get('chat_ask_timeout')} сек."

    await message.answer(report, parse_mode='HTML')
