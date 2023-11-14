'''Handlers for start command'''

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from models.telegram.bot_replicas import BotReplicas
from models.telegram.state import ChooseUserFunctions, ChooseAdminFunctions
from utils.telegram import determine_admin_rights, determine_user_rights

router = Router() 

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    '''Perform user or admin authorization in the bot'''        
    USER_ID = message.from_user.id

    if determine_admin_rights(USER_ID):
        await message.answer("Вы определены как администратор", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ChooseUserFunctions.get_message)
    elif determine_user_rights(USER_ID):
        await message.answer("Вы определены как пользователь", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ChooseAdminFunctions.get_message)
    else:
        await message.answer("Вы не являеетесь пользователем с правом доступа к данному программному обеспечению")
        return

    await state.update_data(is_remember_context=False)
    await state.update_data(converstion_context=list())

    await message.answer(BotReplicas.GREETINGS.value)
