'''
State management model for our drawings
'''

import flet as ft

class State:

    # Costructor
    def __init__(self):

        # Track our previous position for drawing
        self.x: float = float()
        self.y: float = float()

        # Shapes that we are currently drawing so we know what to save to data
        self.lines = []     # Lines
        self.points = []    # Points

        # our list of recent changes so we can undo them
        undo_list = []