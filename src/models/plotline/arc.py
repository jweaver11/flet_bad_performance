from dataclasses import dataclass, field
from typing import Optional, List

# Data class for arcs on a timeline - change to branch as well later??
@dataclass
class Arc:

    title: str  # Required, has no default
    description: str = "Arc Description"

    start_date: Optional[str] = None
    end_date: Optional[str] = None

    involved_characters: List[str] = field(default_factory=list)
                
        