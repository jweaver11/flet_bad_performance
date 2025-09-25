from dataclasses import dataclass, field
from typing import Optional, List


# Data class for plot points on a timeline - change to branch as well later??
@dataclass
class Plot_Point:

    title: str  # Required, has no default
    description: str = "Plot Point Description"   

    date: Optional[str] = None   
    time: Optional[str] = None  

    involved_characters: List[str] = field(default_factory=list)
    related_locations: List[str] = field(default_factory=list)
    related_items: List[str] = field(default_factory=list)

    other: int = 0