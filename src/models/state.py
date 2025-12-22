'''
State management model for our drawings
'''

import flet as ft

class State:

    def __init__(self):

        self.x: float = float()

        self.y: float = float()

        self.lines = []
        self.points = []