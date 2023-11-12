'''All possible states in the FSM aiogram'''

from aiogram.fsm.state import StatesGroup, State


class ChooseUserFunctions(StatesGroup):
    '''Commands that can be used by the user'''
    get_message = State()

class ChooseAdminFunctions(StatesGroup):
    '''Commands that can be used by the user'''
    get_message = State()
