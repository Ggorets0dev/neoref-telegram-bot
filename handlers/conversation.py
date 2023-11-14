'''Handlers for user queries to ChatPGTt'''

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from models.gpt import ChatGpt
from models.telegram.state import ChooseAdminFunctions, ChooseUserFunctions


router = Router()


@router.message(ChooseUserFunctions.get_message)
@router.message(ChooseAdminFunctions.get_message)
async def ask_chat_gpt(message: Message, state: FSMContext):
    '''Get repsonce from ChatGPT'''
    QUERY = message.text
    USER_DATA = await state.get_data()
    IS_REMEMBER_CONTEXT: bool = USER_DATA.get('is_remember_context')

    if IS_REMEMBER_CONTEXT is True:
        conversation = USER_DATA.get('conversation_context')
    else:
        conversation = None

    print(conversation)

    await message.answer("Запрос отправлен")
    
    RESPONSE = ChatGpt.ask(QUERY, conversation)
    
    await message.answer(RESPONSE.last_msg)

    if IS_REMEMBER_CONTEXT is True:
        await state.update_data(conversation_context=RESPONSE.conversation)
