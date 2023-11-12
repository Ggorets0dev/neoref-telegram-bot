'''Handlers for delaccess command'''

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from models.telegram.state import ChooseAdminFunctions
from utils.access import del_access

router = Router()

@router.message(ChooseAdminFunctions.get_message, Command("delaccess"))
async def delaccess_cmd(message: Message):
    '''Add admin to bot'''
    MSG_PARTS = message.text.split()

    if len(MSG_PARTS) != 2:
        await message.answer("Указано неверное количество аргументов команды")
        return
    
    USER_ID: str = MSG_PARTS[-1]
    STATUS = del_access(USER_ID)

    if STATUS:
        await message.answer(f"Доступ для ID {USER_ID} успешно отключен")
    else:
        await message.answer(f"Доступ для ID {USER_ID} не обнаружен")
