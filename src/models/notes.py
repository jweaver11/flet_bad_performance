''' Notes Model for the story object only. Displays in its own widget'''

import flet as ft
import json
import os
from models.app import app
from models.widget import Widget
from constants.data_paths import characters_path

#
class Notes(Widget):
    # Constructor 
    def __init__(self, name, page: ft.Page):
        self.title = name
        self.tag = "notes"
        self.p = page