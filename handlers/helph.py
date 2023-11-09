'''Handlers for help command'''

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from models.telegram.bot_replicas import BotReplicas

router = Router()

@router.message(Command("help"))
async def help_cmd(message: Message):
    '''Show bot information for user'''
    await message.answer(BotReplicas.HELP.value)
