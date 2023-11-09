'''Config class location'''

import os
from typing import Any, Dict, List
import yaml


class Config:
    '''Operations with the configuration file'''
    
    path = None
    
    @staticmethod
    def get(path: str) -> Dict[str, str | int | bool | List[Any]]:
        '''Function to retrieve a configuration file'''
        if not os.path.isfile(path):
            return
        
        with open(path, 'r', encoding='UTF-8') as file_read:
            return yaml.load(file_read, Loader=yaml.FullLoader)
        
    @classmethod
    def get_saved(cls) -> Dict[str, str | int | bool | List[Any]]:
        '''Get the configuration file whose path is saved'''
        if not cls.path:
            raise ValueError("Configuration file path is not saved")
        return cls.get(cls.path)
        
    @staticmethod   
    def set(path: str, config: Dict[str, str | int | bool | List[Any]]) -> None:
        '''Function to save a configuration file'''
        with open(path, 'w', encoding='UTF-8') as file_write:
            yaml.dump(config, file_write, default_flow_style=False)

    @classmethod   
    def set_saved(cls, config: Dict[str, str | int | bool | List[Any]]) -> None:
        '''Save config to saved path'''
        if not cls.path:
            raise ValueError("Configuration file path is not saved")
        return cls.set(cls.path, config)

    @classmethod
    def save_path(cls, path: str) -> None:
        '''Save config path for future get'''
        if not os.path.isfile(path) or not (path.lower().endswith('.yaml') or path.lower().endswith('.yml')):
            raise FileNotFoundError("Incorrect data for working with the file")

        cls.path = path
