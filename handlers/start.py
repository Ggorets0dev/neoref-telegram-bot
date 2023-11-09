'''Handlers for start command'''

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from models.telegram.bot_replicas import BotReplicas
from models.telegram.state import ChooseUserFunctions
from utils.telegram import determine_admin_rights, make_row_keyboard, determine_user_rights

router = Router() 

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    '''Perform user or admin authorization in the bot'''        
    USER_ID = message.from_user.id

    if determine_admin_rights(USER_ID):
        await message.answer("Вы определены как администратор", reply_markup=make_row_keyboard(['Запуск']))
    elif determine_user_rights(USER_ID):
        await message.answer("Вы определены как пользователь", reply_markup=make_row_keyboard(['Запуск']))
    else:
        await message.answer("Вы не являеетесь пользователем с правом доступа к данному программному обеспечению")
        return

    await message.answer(BotReplicas.FAQ.value)
    await state.set_state(ChooseUserFunctions.get_message)
