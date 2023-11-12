'''Handlers for addadmin and adduser commands'''

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from models.telegram.state import ChooseAdminFunctions
from utils.access import add_admin, add_user, check_access

router = Router()

@router.message(ChooseAdminFunctions.get_message, Command("addadmin"))
async def addadmin_cmd(message: Message):
    '''Add admin to bot'''
    MSG_PARTS = message.text.split()

    if len(MSG_PARTS) != 2:
        await message.answer("Указано неверное количество аргументов команды")
        return
    
    USER_ID: str = MSG_PARTS[-1]
    
    if check_access(USER_ID):
        await message.answer("Данный пользователь уже имеет доступ, первым делом отключите его")
        return
    
    add_admin(USER_ID)

    await message.answer(f"Администратор с ID {USER_ID} успешно добавлен")


@router.message(ChooseAdminFunctions.get_message, Command("adduser"))
async def adduser_cmd(message: Message):
    '''Add user to bot'''
    MSG_PARTS = message.text.split()

    if len(MSG_PARTS) != 2:
        await message.answer("Указано неверное количество аргументов команды")
        return
    
    USER_ID: str = MSG_PARTS[-1]

    if check_access(USER_ID):
        await message.answer("Данный пользователь уже имеет доступ, первым делом отключите его")
        return

    add_user(USER_ID)
    
    await message.answer(f"Пользователь с ID {USER_ID} успешно добавлен")
