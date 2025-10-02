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
            self.save_dict(parent)

        self.visible = self.data['visible']

        #self.visible = self.data['visible']

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

        # Load our widget UI on start after we have loaded our data
        self.reload()

    def save_dict(self, parent: Widget):
        ''' Saves our current data to the PARENTS json file '''

        parent.data['mini_widgets'][self.title] = self.data

        parent.save_dict()


    # Called at end of constructor
    def create_default_data(self) -> dict:
        ''' Loads our timeline data and plotlines data from our seperate plotlines files inside the plotlines directory '''
        
        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        return {
            'title': self.title,
            'tag': "mini_note",
        
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            
            'content': "",    # Content of our chapter
        }
    
    # Called when clicking x to hide the mini note
    def toggle_visible(self, e):
        self.visible = not self.visible
        self.p.update()

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Our column that will display our header filters and body of our widget
        self.title_control = ft.TextButton(
            f"Hello from mini note: {self.title}",
            on_click=self.toggle_visible,
        )

        self.content_control = ft.TextField(
            #value=self.data['content'],
            label="Body",
            expand=True,
            multiline=True,
        )

        self.content = ft.Column(
            spacing=6,
            controls=[self.title_control, self.content_control],
        )

        self.p.update()



        