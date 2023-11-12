'''Module for adding and deleting users and admins with command line'''

import argparse
import os
from loguru import logger

from utils.access import add_admin, add_user
from utils.config import Config


# NOTE - Change logger settings
logger.add('logs/access_editor.log', rotation='256 MB')


def main() -> None:
    '''Entry point'''
    # SECTION - Checking config
    CONFIG_PATH = 'config.yaml'

    if os.path.isfile(CONFIG_PATH):
        Config.save_path(CONFIG_PATH)
    else:
        logger.error('Config file was not detected')
        exit(1)
    # !SECTION

    parser = argparse.ArgumentParser(description='Module for adding and deleting users and admins')

    parser.add_argument('-aa', '--add-admin', nargs=1, help='Add new admin to bot (specify Telegram ID)')
    parser.add_argument('-au', '--add-user', nargs=1, help='Add new user to bot (specify Telegram ID)')
    parser.add_argument('-d', '--delete', nargs=1, help='Delete user or admin (specify Telegram ID)')

    ARGS = parser.parse_args()

    print(ARGS)

    if ARGS.add_admin:
        USER_ID = ARGS.add_admin[0]
        add_admin(USER_ID)
        logger.success(f"Admin with ID {USER_ID} added successfully")

    elif ARGS.add_user:
        USER_ID = ARGS.add_user[0]
        add_user(USER_ID)
        logger.success(f"User with ID {USER_ID} added successfully")

    elif ARGS.delete:
        USER_ID = ARGS.delete[0]

    else:
        logger.error("No arguments provided for acces editor")
    
if __name__ == '__main__':
    main()
