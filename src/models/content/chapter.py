import flet as ft
from models.story import Story
from models.widget import Widget


# Class that holds our text chapter objects
class Chapter(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "chapter",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,
        )

        # If no data is passed in (Newly created chapter), give it default data
        if self.data is None:
            self.data = self.create_default_data()  # Create default data if none was passed in
            self.save_dict()

        self.visible = self.data['visible']  # If we will show this widget or not

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()


    # Called at end of constructor
    def create_default_data(self) -> dict:
        ''' Loads our timeline data and plotlines data from our seperate plotlines files inside the plotlines directory '''
        
        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        return {
            'title': self.title,
            'directory_path': self.directory_path,
            'tag': self.tag,
            'pin_location': "bottom",
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it

            'mini_notes': {},
            
            'content': "",    # Content of our chapter
        }
    
    def submit_mini_note(self, e):
        title = e.control.value
        self.create_mini_note(title)
        e.control.value = ""
        self.p.update()

    def create_mini_note(self, title: str):
        ''' Creates a mini note inside an image or chapter '''

        print(title)

        from models.mini_note import MiniNote


        # Add to list
        self.mini_notes.append(MiniNote(title=title, page=self.p))
        
        print(self.mini_notes)

        self.reload_widget()

        #return mini_note


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Our column that will display our header filters and body of our widget
        body = ft.Column([
            ft.Text(f"hello from: {self.title}"),
            ft.TextField(
                label="Create Mini Note",
                hint_text="Type your note here...",
                expand=True,
                on_submit=self.submit_mini_note,
            )
        ])

        # Our stack holds the body under the tab, so put it there
        self.stack.controls.append(body)

        # Column that holds our mini note controls on the right 1/3 of the widget
        mini_notes_column = ft.Column(
            spacing=6,
            controls=self.mini_notes,   # They'll only be rendered if visible
        )

        # Spacing container to give some space between our body and mini notes
        mini_notes_row = ft.Row(expand=True,)

        # Create a spacinig container and add it so our mini notes only take up the right most 1/3 of widget
        spacing_container = ft.Container(expand=True, ignore_interactions=True, bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.RED))
        mini_notes_row.controls.append(spacing_container)
        mini_notes_row.controls.append(spacing_container)
        mini_notes_row.controls.append(mini_notes_column)

        # Add the column on top of our stack
        self.stack.controls.append(mini_notes_row)


        # Our tab content holds the stack that holds our body
        self.tab.content=self.stack  # We add this in combo with our 'tabs' later


        # Sets our actual 'tabs' portion of our widget, since 'tab' needs to nest inside of 'tabs' in order to work
        content = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
        )
        
        # Content of our widget (ft.Container) is our created 'tabs' content
        self.content = content

        self.p.update()

        