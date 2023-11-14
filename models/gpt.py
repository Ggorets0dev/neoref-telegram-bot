'''ChatGpt class location'''

from dataclasses import dataclass
from typing import Dict, List
import openai


class ChatGpt:
    '''Interface for aconnecting and activate prompts to ChatGPT'''

    MODEL: str = "gpt-3.5-turbo"
    api_key: str = None

    @dataclass(frozen=True)
    class Response:
        '''Response from ChatGPT'''
        last_msg: str
        conversation: List[Dict[str, str]]

    @classmethod
    def ask(cls, query: str, conversation: List[Dict[str, str]] = None) -> Response:
        '''Ask a question to ChatGPT'''
        NEW_QUERY = {"role": "user", "content": f"{query}"}
        
        if conversation is not None:
            conversation.append(NEW_QUERY)
        else:
            conversation = [NEW_QUERY]
        
        response = openai.OpenAI(api_key=cls.api_key).chat.completions.create(
            messages = conversation,
            model = cls.MODEL,
            max_tokens=30
        )

        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        RESPONSE = f'{conversation[-1]["content"].strip()}'

        return cls.Response(last_msg=RESPONSE, conversation=conversation)

    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        '''Save api key to bot'''
        cls.api_key = api_key

    @classmethod
    def check_api_key(cls, api_key: str) -> bool:
        '''Check if api key is valid on OpenAI'''
        try:
            openai.OpenAI(api_key=api_key).chat.completions.create(
            messages = [
                {
                    "role": "user",
                    "content": str(),
                }
            ],
            model = cls.MODEL,
            max_tokens=1
        )
        except openai.AuthenticationError:
            return False
        else:
            return True
        