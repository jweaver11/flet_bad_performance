'''
Parent class for mini widgets, which are extended flet containers used as information displays on the side of the parent widget
Makes showing detailed information easier without rending and entire widget where it doesn't make sense
Mini widgets are stored in their OWNERS (Widget) json file, not their own file
'''


import flet as ft
from models.widget import Widget
from handlers.verify_data import verify_data



class MiniWidget(ft.Container):
    # Constructor. All mini widgets require a title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):

        # Parent constructor
        super().__init__(
            expand=True,
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.GREEN),
            data=data,      # Sets our data. NOTE. If data is None, you need to set to {} later
        )

        # Sets our data empty to prevent errors if its none
        if self.data is None or not isinstance(self.data, dict):
            self.data = {}
           
        self.title = title  # Title of the widget that will show up on its tab
        self.owner = owner  # The widget that contains this mini widget. (Can't use parent because ft.Containers have hidden parent attribute)
        self.p = page   # Grabs our original page for convenience and consistency


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our object so we can access its data and change it
            {   # Pass in the required fields and their types
                'title': str,       # Title of the mini widget, should match the object title
                'tag': str,     # Default mini widget tag, but should be overwritten by child classes
                'visible': bool,        # If the widget is visible. Flet has this parameter build in, so our objects all use it
                'is_selected': bool,    # If the mini widget is selected in the owner's list of mini widgets, to change parts in UI
            },
        )

        # Check if we loaded our mini widget or created a new one
        if data is None:
            loaded = False
        else:
            loaded = True

        # If not loaded, set default values. No new data here, just giving values to existing fields
        if not loaded:
            self.data.update({
                'title': self.title,        
                'visible': True,    # Only need to specify bools if True, they default to False
            })
            self.save_dict()


        # Apply our visibility
        self.visible = self.data['visible']
        self.is_selected = False    # Check if we are selected for ui purposes

        # UI Elements
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

    # Called when saving changes in our mini widgets data to the OWNERS json file
    def save_dict(self):
        ''' Saves our current data to the OWNERS json file '''

        # Error Handling
        if self.owner.data is None or not isinstance(self.data, dict):
            print("Error: owner data is None, cannot save mini widget data")
            return
        
        # TODO: Run through all values in owners mini widgets dictionary. If tag, owner, and title match, save there
        # -- issue when renaming mini widgets. But thats for later. Save before renaming and should be fine



        # This works in widgets that only have simple mini widgets (like chapters and characters).
        # Widgets that store mini Widgets nested in other Mini Widgets (like timelines with branches) will need to override this function
        # Grab our owner object, and update their data pertaining to this mini widget
        self.owner.data['mini_widgets'][self.title] = self.data

        # Save our owners json file to match their data
        self.owner.save_dict()


    # Called when clicking x to hide the mini note
    def toggle_visibility(self, e):
        ''' Shows or hides our mini widget, depending on current state '''

        print(f"Toggling visibility for mini widget: {self.title}")

        self.data['visible'] = not self.data['visible']
        self.visible = self.data['visible']
        
        self.save_dict()
        self.p.update()

        print(f"Mini widget: {self.title} visibility is now: {self.visible}")

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_mini_widget(self):
        ''' Reloads our mini widget UI based on our data '''

        # Create body content
        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
            ],
            expand=True,
        )

        self.render_mini_widget()

    def render_mini_widget(self):
        ''' Renders our mini widget UI based on our data '''

        # Give Uniform mini titles andd styling

        self.p.update()

        