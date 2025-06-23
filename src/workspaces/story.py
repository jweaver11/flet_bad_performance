''' Master Story/Project class for projects'''
import flet as ft
from workspaces.character.character import Character, create_character_widget
from handlers.layout_widgets import layout_widgets


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story
        self.visible_widgets = {} # dict of widget objects (ft cont.) and a bool value
        self.characters = {}    # dict of characters name = name of character object

        
    # Method to add new character object to story object
    def create_character(self, name):
        self.characters.update({name: Character(name)})
        # create character widget inside char dict and add to vis widgets
        self.characters[name].widget = create_character_widget(name)
        self.visible_widgets[name] = self.characters[name].widget, True   # auto open new widgets on creation
        self.reload_widgets()

        
    # Check if widgets are visible, return a list of them to layout
    def reload_widgets(self):
        vis_widgets = []
        for name, (widget, visible) in self.visible_widgets.items():
            if visible == True:        # This line is the error
                vis_widgets.append(widget)    # Make our list current with visible widgets

        layout_widgets(vis_widgets) # layout our widgets, and update everything


    def hide_widget(self, widget_name):
        self.visible_widgets[widget_name].visible = False
        self.reload_widgets(self)

    def delete_widget(self, widget_name):
        print("do somethn")

    
    def reorder_widgets(self):
        # mess with position of active_widgets elements
        return(print("reorder_widgets was called"))
        

    # Workspaces within each story object
    # Content
    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??


story = Story("Story Title") 
story.create_character("joe")
story.create_character("bob")