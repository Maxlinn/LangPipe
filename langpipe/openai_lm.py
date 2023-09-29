import sys
import importlib
import time
import json
from typing import List
from dataclasses import dataclass

@dataclass
class ChatGPTConfig:
    model: str = 'gpt-3.5-turbo'
    api_key: str = ''
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0


class ChatGPTForConvLM:    
        
    def __init__(self, config: ChatGPTConfig) -> None:
        self.config = config
        self.last_response = None
        
        name = 'openai'
        if name in sys.modules:
            self.openai = importlib.reload(sys.modules[name])
        else:
            self.openai = importlib.import_module(name)
        self.openai.api_key = self.config.api_key
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({str(self.config)})"
    
    def __repr__(self) -> str:
        return self.__str__()
        
    # https://platform.openai.com/docs/guides/gpt/chat-completions-api
    def generate(self,
                 conv:list,
                 system:str='',
                 **kwargs
                 )->List[str]:
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        for i, turn in enumerate(conv):
            role = 'user' if i % 2 == 0 else 'assistant'
            messages.append({'role': role, 'content': turn})
        
        response :dict = self.openai.Completion.create(
            model=self.config.model,
            messages=messages,
            **kwargs
        )
        self.last_response = response
        
        # save usage
        self.config.completion_tokens += response['usage']['completion_tokens']
        self.config.prompt_tokens += response['usage']['prompt_tokens']
        self.config.total_tokens += response['usage']['total_tokens']
        
        replys = []
        for choice in response['choices']:
            reason = choice['finish_reason']
            # skip abnormal completion
            if reason not in ('stop', 'length', 'function_call'):
                continue

            # index = choice['index']
            content = choice['message']['content']
            replys.append(content)
        
        return replys
    
    
    def generate_retry(self,
                        max_tries=3,
                        delay=5,
                        **generate_kwargs):
        ret = []
        for trial in range(max_tries):
            try:
                ret = self.generate(**generate_kwargs)
            except Exception as e:
                if 'RateRateLimitError' in repr(e):
                    time.sleep(delay)
                    continue
                else:
                    raise e
            else:
                # abnormally no response
                if not ret:
                    break               
            
        return ret
        
    
    def save_json(self, save_path:str):
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    
    
    @staticmethod
    def from_json(json_path:str):
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        obj = ChatGPTForConvLM(config=config)
        return obj