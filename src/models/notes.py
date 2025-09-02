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


import flet as ft
import json
import os
#import data_paths
from models.widget import Widget
from constants.data_paths import notes_path

class Notes(Widget):
    def __init__(self, title: str):
        #might remove title
        self.title = title # Title of the notes
        self.content = ""  # Content of the notes
        self.created_at = ft.datetime.now()  # Creation timestamp
        self.updated_at = ft.datetime.now()  # Last updated timestamp
        
        #data_paths.set_active_story_path(title)
       
        self.file_path = os.path.join(notes_path, f"{self.title}.json")
        # ^ recommended
        #self.file_path = data_paths.active_story_path
        #^ import data path doesn't work and this doesn't work w/o doing that

        # Metadata for the note
        self.metadata = {
            "title": self.title,
            "character_count": int,
            "created_at": None,
            "last_modified": None
        }
        