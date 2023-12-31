'''General operations-shortcuts for telegram api'''

from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models.hasher import Hasher

from utils.config import Config


def make_row_keyboard(items: List[str], input_field_placeholder: str = 'Выбор') -> ReplyKeyboardMarkup:
    '''Make keyboard with one row'''
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True, input_field_placeholder=input_field_placeholder)


def make_column_keyboard(items: List[str], input_field_placeholder: str = 'Выбор') -> ReplyKeyboardMarkup:
    '''Make keyborad with one column'''
    column = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=column, resize_keyboard=True, input_field_placeholder=input_field_placeholder)


def determine_admin_rights(user_id: int) -> bool:
    '''Check if the user has administrator rights'''
    CONFIG = Config.get_saved()
    ADMIN_IDS = CONFIG.get('admin_ids') or list()
    HASHER = Hasher()

    user_id = str(user_id).encode()

    is_admin = False
    for ID in ADMIN_IDS:
        if HASHER.verify_hash(value=user_id, value_hash=ID.encode()):
            is_admin = True
            break

    return is_admin


def determine_user_rights(user_id: int) -> bool:
    '''Check if user is in accepted users'''
    CONFIG = Config.get_saved()
    USER_IDS = CONFIG.get('user_ids') or list()
    HASHER = Hasher()

    user_id = str(user_id).encode()

    is_user = False
    for ID in USER_IDS:
        if HASHER.verify_hash(value=user_id, value_hash=ID.encode()):
            is_user = True
            break

    return is_user
