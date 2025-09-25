from dataclasses import dataclass

@dataclass
class Plotpoint:
    def __init__(self, title: str):

        self.title: str = title  # Required, has no default
        self.description: str = "Event Description"   # Defaults to 'Event Description'

        self.date: str = None   # These are 'points' on the timeline, so they just get a date, not a start/end range
        self.time: str = None   # Time during that day

        self.involved_characters: list = []
        self.related_locations: list = []
        self.related_items: list = []

        self.other: int = None