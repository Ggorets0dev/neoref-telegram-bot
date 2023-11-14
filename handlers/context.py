'''Handlers for commands remember, forget, clear'''

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from models.telegram.state import ChooseUserFunctions, ChooseAdminFunctions

router = Router()

@router.message(ChooseUserFunctions.get_message, Command("remember"))
@router.message(ChooseAdminFunctions.get_message, Command("remember"))
async def remember_context(message: Message, state: FSMContext):
    '''Start remembering context for user'''
    USER_DATA = await state.get_data()

    if USER_DATA.get('is_remember_context') is False:
        await state.update_data(is_remember_context=True)
        await message.answer("Запоминание контекста включено")
    else:
        await message.answer("Запоминание контекста уже находится во включенном состоянии")


@router.message(ChooseUserFunctions.get_message, Command("forget"))
@router.message(ChooseAdminFunctions.get_message, Command("forget"))
async def forget_context(message: Message, state: FSMContext):
    '''Start remembering context for user'''
    USER_DATA = await state.get_data()

    if USER_DATA.get('is_remember_context') is True:
        await state.update_data(is_remember_context=False)
        await state.update_data(conversation_context=list())
        await message.answer("Запоминание контекста отключено, история запросов очищена")
    else:
        await message.answer("Запоминание контекста уже находится в отключенном состоянии")
    

@router.message(ChooseUserFunctions.get_message, Command("clear"))
@router.message(ChooseAdminFunctions.get_message, Command("clear"))
async def clear_context(message: Message, state: FSMContext):
    '''Start remembering context for user'''
    USER_DATA = await state.get_data()

    if USER_DATA.get('is_remember_context') is True:
        await state.update_data(conversation_context=list())
        await message.answer("История запросов очищена")
    else:
        await message.answer("Запоминание контекста находится в отключенном состоянии, нет истории для очистки")
