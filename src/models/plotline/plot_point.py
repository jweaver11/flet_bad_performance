from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Plot_Point:
    title: str  # Required, has no default
    description: str = "Plot Point Description"   

    date: Optional[str] = None   # These are 'points' on the timeline, so they just get a date, not a start/end range
    time: Optional[str] = None   # Time during that day

    involved_characters: List[str] = field(default_factory=list)
    related_locations: List[str] = field(default_factory=list)
    related_items: List[str] = field(default_factory=list)

    other: int = 0