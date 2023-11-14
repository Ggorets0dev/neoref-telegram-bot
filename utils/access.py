'''Functionality for changing acces to bot'''

from typing import List

from loguru import logger
from models.hasher import Hasher
from utils.config import Config


def add_admin(user_id: str) -> None:
    '''Add admin to configuraion file'''
    HASHED_USER_ID = Hasher().hash_with_argon2id(user_id.encode(), Hasher.NORMAL_HASHING_PRESET)
    config = Config.get_saved()

    if config is not None:
        admin_ids = config.get('admin_ids') or list()
    else:
        config = dict()
        admin_ids = list()
    
    admin_ids.append(HASHED_USER_ID)
    config['admin_ids'] = admin_ids
    Config.set_saved(config)

    logger.success(f"Admin with ID {user_id} added successfully")

def add_user(user_id: str) -> None:
    '''Add user to configuration file'''
    HASHED_USER_ID = Hasher().hash_with_argon2id(user_id.encode(), Hasher.LIGHT_HASHING_PRESET)
    config = Config.get_saved()

    if config is not None:
        user_ids = config.get('user_ids') or list()
    else:
        config = dict()
        user_ids = list()
    
    user_ids.append(HASHED_USER_ID)
    config['user_ids'] = user_ids
    Config.set_saved(config)

    logger.success(f"User with ID {user_id} added successfully")

def check_access(user_id: str) -> bool:
    '''Check if user is in aby group'''
    HASHER = Hasher()
    CONFIG = Config.get_saved()

    if CONFIG is None:
        return False

    user_id = user_id.encode()    
    ALL_IDS: List[str] = (CONFIG.get('user_ids') or list()) + (CONFIG.get('admin_ids') or list())

    for uid in ALL_IDS:
        if HASHER.verify_hash(user_id, uid.encode()):
            return True
        
    return False

def del_access(user_id: str) -> bool:
    '''Delete ID from user or admin'''
    HASHER = Hasher()

    config = Config.get_saved()
    
    # SECTION - Delete user if it exists
    user_ids: List[str] = config.get('user_ids') or list()

    is_found = False

    for inx, uid in enumerate(user_ids):
        if HASHER.verify_hash(user_id.encode(), uid.encode()):
            user_ids.pop(inx)
            is_found = True

    config['user_ids'] = user_ids
    # !SECTION

    # SECTION - Delete admin if it exists
    if not is_found:
        admin_ids: List[str] = config.get('admin_ids') or list()

        for inx, uid in enumerate(admin_ids):
            uid = str(uid)
            if HASHER.verify_hash(user_id.encode(), uid.encode()):
                admin_ids.pop(inx)
                is_found = True

        config['admin_ids'] = admin_ids
        Config.set_saved(config)
    # !SECTION

    if is_found:
        logger.success(f"Access with ID {user_id} deleted successfully")
    else:
        logger.info(f"Access with ID {user_id} not found")

    return is_found
