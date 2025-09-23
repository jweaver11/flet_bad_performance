

class Plotpoint:
    def __init__(self, title: str):

        self.title = title  # Set our title
        self.description = "Event Description"

        self.date = None   # These are 'points' on the timeline, so they just get a date, not a start/end range
        self.time = None   # Time during that day

        self.involved_characters = []
        self.related_locations = []
        self.related_items = []