from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Time_Skip:

    title: str  # Required, has no default
    
    start_date: Optional[str] = None   # Start and end date of this particular plot
    end_date: Optional[str] = None
        