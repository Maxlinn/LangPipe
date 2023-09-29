from .prompt import AbstractPrompt
from typing import List


class PromptBuilder(AbstractPrompt):
    
    def __init__(self, *segments, delimiter='\n\n'):
        self.segments :List[AbstractPrompt] = segments
        self.delimiter = delimiter
    
    def __str__(self):
        segment_strs = list(map(str, self.segments))
        return self.delimiter.join(segment_strs)
    