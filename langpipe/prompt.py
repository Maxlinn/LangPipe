from abc import ABC
from typing import List, Optional


class AbstractPrompt(ABC):
    
    def __str__(self):
        return NotImplementedError
    def __repr__(self):
        return f'{self.__class__.__name__}({str(self)})'


class Prompt(AbstractPrompt):
    
    def __init__(self, prompt:str) -> None:
        super().__init__()
        self.prompt = prompt
    
    def __str__(self) -> str:
        return self.prompt
    
    @staticmethod
    def from_prompts(*prompts, delimiter='\n\n'):
        prompts = list(map(str, prompts))
        return delimiter.join(prompts)
    

class RolePrompt(AbstractPrompt):
    
    def __init__(self, role:str):
        super().__init__()
        self.role = role
        
    def __str__(self) -> str:
        return f'Assume you are a {self.role}.'
    

class TaskPrompt(AbstractPrompt):
    def __init__(self, task:str):
        super().__init__()
        self.task = task
        
    def __str__(self):
        return f'Your task is to {self.task}.'


class FewShotPrompt(AbstractPrompt):
    
    def __init__(self, examples:list):
        super().__init__()
        assert examples, 'FewShotPrompt needs at least one example.'
        self.examples = examples

    def __str__(self) -> str:
        if len(self.examples) == 1:
            prompt = 'Here is an exmaple:\n'
        else:
            prompt = 'Here are some examples:\n'
            examples_s = [f'example {i+1}: {example}' 
                          for i, example in enumerate(self.examples)]
            prompt += '\n'.join(examples_s)
        return prompt


class NoOtherWordsPrompt(AbstractPrompt):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return 'Reply as requested, NO OTHER WORDS.'


class RequestDictPrompt(AbstractPrompt):
    
    def __init__(self, 
                 keys :List[str], 
                 descs :Optional[List[str]], 
                 count=1):
        '''
        :param keys: the keys of dict to be generated.
        :param descs: the desctiptions of the keys.
        :param many: request how many dicts, count can be greater than zero or -1(best effort).
        '''
        super().__init__()
        if descs is not None:
            assert len(keys) == len(descs), 'descriptions should have same length as keys.'
        assert count > 0 or count == -1, 'count can be greater than zero or -1(as more as gpt can)'
        
        self.keys = keys
        self.descs = descs
        self.count = count
        
        
    def __str__(self):
        prompt = 'Your reply should be in key: value manner.'
        
        if self.count:
            prompt += ' When return multiple occurences, add a newline between occurences.'
            if self.count != -1:
                prompt += f' Reply {self.count} occurences.'
            else:
                prompt += ' Reply as much occurences as you can.'
        
        # no key descriptions, gpt will guess from the key names
        if self.descs is None:
            keys_s = ', '.join(self.keys)
            prompt += f' The keys are as follows: {keys_s}.'
        else:
            prompt += ' The keys and their descriptions are as following:\n'
            
            k_descs_s = []
            for key, desc in zip(self.keys, self.descs):
                desc = desc if desc else '[description not provided]'
                k_descs_s.append(f'{key}: {desc}')
            s += '\n'.join(k_descs_s)
        return s