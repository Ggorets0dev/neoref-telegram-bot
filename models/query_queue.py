'''QueryQueue class location'''

from typing import Dict, List
from loguru import logger

class QueryQueue:
    '''Data about currently running requests in ChatGPT'''

    query_limit = 1

    def __init__(self, queries: List[Dict[int, str]] = None) -> None:        
        self.__queries = queries or dict()

    @classmethod
    def set_query_limit(cls, query_limit: int) -> None:
        '''Set global query limit'''
        cls.query_limit = query_limit

    @property
    def queries(self):
        '''Return queries from queue'''
        return self.__queries

    def is_full(self) -> bool:
        '''Check if theres no place in queue'''
        return len(self.__queries) >= self.query_limit
    
    def is_in_progress(self, user_id: int) -> bool:
        '''Check if request for user is in progress'''
        return user_id in self.__queries

    def add_query(self, user_id: int, query: str) -> None:
        '''Add query to queue'''
        if len(self.__queries) >= self.query_limit:
            raise ValueError("There is no space for new query in queue")

        self.__queries[user_id] = query
        logger.info(f"Query from user with ID {user_id} added to queue")

    def delete_query(self, user_id: int) -> None:
        '''Delete query from queue'''
        self.__queries.pop(user_id)
        logger.info(f"Query from user with ID {user_id} removed from queue")
