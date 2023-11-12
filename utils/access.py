'''Functionality for changing acces to bot'''

from models.hasher import Hasher
from utils.config import Config


def add_admin(user_id: str) -> None:
    '''Add admin to configuraion file'''
    HASHED_USER_ID = Hasher().hash_with_argon2id(user_id.encode(), Hasher.NORMAL_HASHING_PRESET)
    config = Config.get_saved()
    config['admin_ids'].append(HASHED_USER_ID)
    Config.set_saved(config)

def add_user(user_id: str) -> None:
    '''Add user to configuration file'''
    HASHED_USER_ID = Hasher().hash_with_argon2id(user_id.encode(), Hasher.LIGHT_HASHING_PRESET)

    config = Config.get_saved()
    user_ids = config.get('user_ids') or list()
    user_ids.append(HASHED_USER_ID)
    config['user_ids'] = user_ids
    Config.set_saved(config)
    