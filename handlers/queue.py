'''Handlers for queue command'''

from aiogram import Router, html
from aiogram.types import Message
from aiogram.filters import Command
from handlers.conversation import query_queue
from models.telegram.state import ChooseAdminFunctions

router = Router()

@router.message(ChooseAdminFunctions.get_message, Command("queue"))
async def queue_cmd(message: Message):
    '''Show bot information for user'''
    queue_report = str()

    for user_id, query in query_queue.queries.items():
        queue_report += f"{html.bold('ID: ')} {user_id}"
        queue_report += '\n'
        queue_report += f"{html.bold('Запрос: ')} {query}"
        queue_report += '\n\n'

    if queue_report:
        await message.answer(queue_report, parse_mode='HTML')
    else:
        await message.answer("Запросы в очереди отсутствуют")
