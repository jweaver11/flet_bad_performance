from dataclasses import dataclass, field
from typing import Optional, List

@dataclass

class Timeskips:
    def __init__(self, title: str):
        self.data = {
            'title': title, 
            'start_date': None, 
            'end_date': None
        }
        