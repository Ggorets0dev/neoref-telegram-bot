'''Handlers for user queries to ChatPGTt'''

from loguru import logger
import openai

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

    await message.answer("Запрос отправлен")
    
    try:
        RESPONSE = ChatGpt.ask(QUERY, conversation)

    except openai.APITimeoutError:
        await message.answer("Не удалось получить ответ от модели в отведенный срок, пожалуйста, повторите запрос")
        logger.error(f"For the user with ID {message.from_user.id} failed to execute the request within the allotted period")
    
    else:
        await message.answer(RESPONSE.last_msg)
        logger.info(f"For the user with ID {message.from_user.id} a response was sent to the request")

        if IS_REMEMBER_CONTEXT is True:
            await state.update_data(conversation_context=RESPONSE.conversation)
