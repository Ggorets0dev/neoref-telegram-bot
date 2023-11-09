'''Handlers for addadmin and adduser commands'''

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from models.hasher import Hasher
from models.telegram.state import ChooseUserFunctions
from utils.config import Config
from utils.telegram import determine_admin_rights

router = Router()

@router.message(ChooseUserFunctions.get_message, Command("addadmin"))
async def addadmin_cmd(message: Message):
    '''Add admin to bot'''
    MSG_PARTS = message.split()

    if not determine_admin_rights(message.from_user.id):
        await message.answer("Добавление администраторов доступно только другим администраторам")
        return 

    elif len(MSG_PARTS) != 2:
        await message.answer("Указано неверное количество аргументов команды")
        return
    
    USER_ID: str = MSG_PARTS[-1]
    HASHED_USER_ID = Hasher().hash_with_argon2id(USER_ID.encode(), Hasher.NORMAL_HASHING_PRESET)

    Config.add_saved({'admin_ids': [HASHED_USER_ID]})
    await message.answer(f"Администратор с ID {USER_ID} успешно добавлен")


@router.message(ChooseUserFunctions.get_message, Command("adduser"))
async def adduser_cmd(message: Message):
    '''Add user to bot'''
    MSG_PARTS = message.split()

    if not determine_admin_rights(message.from_user.id):
        await message.answer("Добавление пользователей доступно только администраторам")
        return

    elif len(MSG_PARTS) != 2:
        await message.answer("Указано неверное количество аргументов команды")
        return
    
    USER_ID: str = MSG_PARTS[-1]
    HASHED_USER_ID = Hasher().hash_with_argon2id(USER_ID.encode(), Hasher.LIGHT_HASHING_PRESET)

    Config.add_saved({'user_ids': [HASHED_USER_ID]})
    await message.answer(f"Пользователь с ID {USER_ID} успешно добавлен")
