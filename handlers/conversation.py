'''Handlers for user queries to ChatPGTt'''

import asyncio
import threading
from typing import Dict
from loguru import logger
import openai

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from models.gpt import ChatGpt
from models.telegram.state import ChooseAdminFunctions, ChooseUserFunctions


user_ids_in_progress = list()

router = Router()


@router.message(ChooseUserFunctions.get_message)
@router.message(ChooseAdminFunctions.get_message)
async def ask_chat_gpt(message: Message, state: FSMContext):
    '''Get repsonce from ChatGPT'''
    def thread_target(QUERY: str, IS_REMEMBER_CONTEXT: bool, CONVERSATION_CONTEXT: Dict[str, str], STATE, USER_ID: int, LOOP, BOT):
        '''Send request to ChatGPT'''
        asyncio.run_coroutine_threadsafe(BOT.send_message(USER_ID, 'Запрос отправлен'), LOOP)
        
        try:
            RESPONSE = ChatGpt.ask(QUERY, CONVERSATION_CONTEXT)

        except openai.APITimeoutError:
            asyncio.run_coroutine_threadsafe(BOT.send_message(USER_ID, "Не удалось получить ответ от модели в отведенный срок, пожалуйста, повторите запрос"), LOOP)
            logger.error(f"For the user with ID {message.from_user.id} failed to execute the request within the allotted period")
        
        else:
            asyncio.run_coroutine_threadsafe(BOT.send_message(USER_ID, RESPONSE.last_msg), LOOP)
            logger.info(f"For the user with ID {message.from_user.id} a response was sent to the request")

            if IS_REMEMBER_CONTEXT is True:
                asyncio.run_coroutine_threadsafe(STATE.update_data(conversation_context=RESPONSE.conversation), LOOP)

        finally:
            user_ids_in_progress.remove(USER_ID)

    QUERY = message.text
    USER_ID = message.from_user.id
    
    if USER_ID in user_ids_in_progress:
        await message.answer("Один запрос от Вас уже находится в работе, пожалуйста, ожидайте ответа")
        return
    else:
        user_ids_in_progress.append(USER_ID)

    BOT = message.bot
    LOOP = asyncio.get_event_loop()
    
    USER_DATA = await state.get_data()
    IS_REMEMBER_CONTEXT = USER_DATA.get('is_remember_context')
    CONVERSATION_CONTEXT = USER_DATA.get('conversation_context') if IS_REMEMBER_CONTEXT is True else None

    new_thread = threading.Thread(target=thread_target, args=[QUERY, IS_REMEMBER_CONTEXT, CONVERSATION_CONTEXT, state, USER_ID, LOOP, BOT])
    new_thread.start()
