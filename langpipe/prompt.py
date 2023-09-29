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
            s = 'Here is an exmaple:\n'
        else:
            s = 'Here are some examples:\n'
            example_strs = [f'Example {i+1}: {example}' for i, example in enumerate(self.examples)]
            s += '\n'.join(example_strs)
        return s


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
        assert count > 0 or count == -1, 'count can be greater than zero or -1(best effort)'
        
        self.keys = keys
        self.descs = descs
        self.count = count
        
        
    def __str__(self):
        s :str = 'Your reply should be in key: value manner.'
        
        if self.count:
            s += ' When return multiple occurences, add a newline between occurences.'
            if self.count == -1:
                s += ' Reply as much occurences as you can.'
            else:
                s += f' Reply {self.count} occurences.'
        
        if self.descs is None:
            key_strs = ', '.join(self.keys)
            s += f' The keys are as follows: {key_strs}.'
        else:
            s += ' The keys and their descriptions are as following:\n'
            
            k_desc_strs = ['{key}: {desc}'.format(
                                key=key,
                                desc = desc if desc else '[description not provided]'
                            ) 
                           for key, desc in zip(self.keys, self.descs)]
            s += '\n'.join(k_desc_strs)
        return s