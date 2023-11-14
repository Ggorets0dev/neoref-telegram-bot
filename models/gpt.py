'''ChatGpt class location'''

from dataclasses import dataclass
from typing import Dict, List
import openai
from loguru import logger

class ChatGpt:
    '''Interface for aconnecting and activate prompts to ChatGPT'''

    model: str = None
    api_key: str = None
    max_tokens: int = None
    check_timeout_sec: int = None
    ask_timeout_sec: int = None

    @dataclass(frozen=True)
    class Response:
        '''Response from ChatGPT'''
        last_msg: str
        conversation: List[Dict[str, str]]

    @classmethod
    def ask(cls, query: str, conversation: List[Dict[str, str]] = None) -> Response:
        '''Ask a question to ChatGPT'''
        if not cls.max_tokens or not cls.api_key:
            raise ValueError("Not all data has been initialized to work with ChatGPT")
        
        NEW_QUERY = {"role": "user", "content": f"{query}"}
        
        if conversation is not None:
            conversation.append(NEW_QUERY)
        else:
            conversation = [NEW_QUERY]
        
        response = openai.OpenAI(api_key=cls.api_key).chat.completions.create(
            messages = conversation,
            model = cls.model,
            max_tokens = cls.max_tokens,
            timeout=cls.ask_timeout_sec
        )

        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        RESPONSE = f'{conversation[-1]["content"].strip()}'

        return cls.Response(last_msg=RESPONSE, conversation=conversation)

    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        '''Save api key to bot'''
        cls.api_key = api_key
    
    @classmethod
    def set_max_tokens(cls, max_tokens: int) -> None:
        '''Save api key to bot'''
        cls.max_tokens = max_tokens

    @classmethod
    def set_model(cls, model: str) -> None:
        '''Save api key to bot'''
        cls.model = model   

    @classmethod
    def set_timeouts(cls, check_timeout_sec: int, ask_timeout_sec: int) -> None:
        '''Save api key to bot'''
        cls.check_timeout_sec = check_timeout_sec
        cls.ask_timeout_sec = ask_timeout_sec

    @classmethod
    def check_api_key(cls, api_key: str, tries_cnt: int) -> bool:
        '''Check if api key is valid on OpenAI'''
        while tries_cnt > 0:
            try:
                openai.OpenAI(api_key=api_key).chat.completions.create(
                messages = [
                    {
                        "role": "user",
                        "content": str(),
                    }
                ],
                model = "gpt-3.5-turbo",
                max_tokens = 1,
                timeout = cls.check_timeout_sec
            )
            except openai.AuthenticationError:
                return False
            except openai.APITimeoutError:
                logger.warning("Failed to receive a response within the allotted time, reconnecting...")
                tries_cnt -= 1
            else:
                return True
        
        return False
    