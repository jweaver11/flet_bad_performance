'''
Parent class for mini widgets, which are extended flet containers used as information displays on the side of the parent widget
Makes showing detailed information easier without rending and entire widget where it doesn't make sense
Mini widgets are stored in their OWNERS (Widget) json file, not their own file
Some mini widgets can have their own files IN ADDITION to normal storage, such as maps or drawings storing images
'''


import flet as ft
from models.widget import Widget
from handlers.verify_data import verify_data


class MiniWidget(ft.Container):

    # Constructor. All mini widgets require a title, owner widget, father (parent), page reference...
    # Dictionary path, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father, page: ft.Page, dictionary_path: str, data: dict=None):

        # Parent constructor
        super().__init__(
            expand=True,
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.GREEN),
            data=data,      # Sets our data.
        )
           
        self.title = title                          # Title of the widget that will show up on its tab
        self.owner = owner                          # The widget that contains this mini widget.
        self.father = father                        # Immidiate parent object that holds us (Can't use 'parent' cuz flet)
        self.p = page                               # Grabs our original page for convenience and consistency
        self.dictionary_path = dictionary_path      # Path to our dict within our fathers data


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our object so we can access its data and change it
            {   
                'title': self.title,    # Title of the mini widget, should match the object title
                'tag': "mini_widget",   # Default mini widget tag, but should be overwritten by child classes
                'visible': True,        # If the widget is visible
                'is_selected': bool,    # If the mini widget is selected in the owner's list of mini widgets, to change parts in UI
            },
        )

        # Apply our visibility
        self.visible = self.data['visible']
        self.is_selected = False    # Check if we are selected for ui purposes

        # Control for our title
        self.title_control = ft.TextField(
            value=self.title,
            label=None,
        )

        # Control for our content/body
        self.content_control = ft.TextField(
            label="Body",
            expand=True,
            multiline=True,
        )

    # Called when saving changes in our mini widgets data to the OWNERS json file
    def save_dict(self):
        ''' Saves our current data to the OWNERS json file using this objects dictionary path '''

        try:
        
            # If our data is None (we just got deleted), we don't save ourselves to fathers data
            if self.data is None:
                pass

            # Otherwise, save like normal
            else:

                # Our data is correct, so we update our immidiate parents data to match
                self.father.data[self.dictionary_path][self.title] = self.data

            # Recursively updates the parents data until father=owner (widget), which saves to file
            self.father.save_dict()
            
            # This keeps everyones data in sync so we can infinitely nest mini widgets if we want, like for arcs in timelines

        except Exception as e:
            print(f"Error saving mini widget data to {self.title}: {e}")
            

    # Called when deleting our mini widget
    def delete_dict(self):
        ''' Deletes our data from all live widget/mini widget objects that we nest in, and saves the owners file '''

        try:

            # Remove our data
            self.data = None

            # Remove the data of our father (parent) widget/mini widget to match
            # By deleting the father data manually here, it will cascade up the chain when save_dict is called
            self.father.data[self.dictionary_path].pop(self.title, None)
            
            # Applies the changes up the chain
            self.save_dict()

            # Applies the UI changes by removing ourselves from the mini widgets list
            if self in self.owner.mini_widgets:
                self.owner.mini_widgets.remove(self)
            
            # Reload the widget if we have to
            if self.visible:
                self.owner.reload_widget()

            # Also reload the active rail to reflect changes
            self.owner.story.active_rail.content.reload_rail() 

        # Catch errors
        except Exception as e:
            print(f"Error deleting mini widget {self.title}: {e}")
        

    # Called when clicking x to hide the mini widget
    def toggle_visibility(self, e):
        ''' Shows or hides our mini widget, depending on current state '''
       
        # Switch our visibility in data, then apply it
        self.data['visible'] = not self.data['visible']
        self.visible = self.data['visible']
        
        # Save the switch and reflect it in the UI
        self.save_dict()
        self.p.update()


    # Called whenever we hover over our mini widget on the right as a psuedo focus
    def on_hover(self, e: ft.HoverEvent):
        print(e)

        
    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_mini_widget(self):
        ''' Reloads our mini widget UI based on our data '''

        # Add option to have the mini widget show on larger portion of screen, like an expand button at bottom left or right

        # Create body content
        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
            ],
            expand=True,
        )

        # Call render function
        self._render_mini_widget()

    def _render_mini_widget(self):
        ''' Renders our mini widget UI based on our data '''

        # Give Uniform mini titles and styling

        self.p.update()

        