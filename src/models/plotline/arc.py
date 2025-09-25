from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Arc:
    def __init__(self, title: str):
        self.data = {
            
            'title': "Arc Title",
            'description': "Arc Description",
            'start_date': None,
            'end_date': None,
            'involved_characters': [],
                
        }