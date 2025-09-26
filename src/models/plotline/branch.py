from dataclasses import dataclass, field
from typing import Optional, List


# Data class for plot points on a timeline - change to branch as well later??
@dataclass
class Branch:

    title: str  # Required, has no default
    description: str = "Plot Point Description"   

    start_date: Optional[str] = None
    end_date: Optional[str] = None   

    involved_characters: List[str] = field(default_factory=list)
    related_locations: List[str] = field(default_factory=list)
    related_items: List[str] = field(default_factory=list)

    other: str = ""