import flet as ft
from models.story import Story
import os
import json
from models.widget import Widget


# Parent Class that holds our mini note objects (ft.Containers), that are held within widget objects only
# These child objects appear inside of another widget, (from right or left) to show more detail and child information
# Example, clicking a plotpoint, arc, etc. on a timeline brings up a mini widget
class MiniWidget(ft.Container):
    # Constructor
    def __init__(self, title: str, parent: Widget, page: ft.Page, data: dict = None, ):

        super().__init__(
            expand=True,
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.GREEN),
        )
           
        self.title = title  # Title of the widget that will show up on its tab
        self.p = page   # Grabs our original page for convenience and consistency
        self.data = data    # Pass in our data when loading existing mini widgets
        self.parent = parent

        # If no data is passed in (Newly created mini note), give it default data
        if self.data is None:
            self.data = self.create_default_data()  # Create default data if none was passed in
            self.save_dict()

        # Apply our vsibility
        self.visible = self.data['visible']

        self.title_control = ft.TextField(
            value=self.title,
            label=None,
        )

        self.content_control = ft.TextField(
            #value=self.data['content'],
            label="Body",
            expand=True,
            multiline=True,
        )

    # Called when saving changes in our mini widgets data to the PARENTS json file
    def save_dict(self):
        ''' Saves our current data to the PARENTS json file '''

        # TODO PARENT DATA IS BEING PASSED IN AS NONE
        if self.parent.data is None:
            print("Error: Parent data is None, cannot save mini widget data")
            return

        if self.parent.data['mini_widgets'] is None:
            self.parent.data['mini_widgets'] = {}

        # Grab our parent object, and update their data pertaining to this mini widget
        self.parent.data['mini_widgets'][self.title] = self.data

        # Save our parents json file to match their data
        self.parent.save_dict()



    # Called at end of constructor
    def create_default_data(self) -> dict:
        ''' Loads our timeline data and plotlines data from our seperate plotlines files inside the plotlines directory '''
        
        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        return {
            'title': self.title,
            'tag': "",
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            'content': "",    # Content of our chapter
        }



        