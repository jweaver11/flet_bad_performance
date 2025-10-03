import flet as ft
from models.story import Story
from models.widget import Widget


# Class that holds our text chapter objects
class Chapter(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):

        # Check if we're loading a chapter or creating a new one
        if data is None:
            loaded = False
        else:
            loaded = True
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "chapter",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # This gets initialized at the end of our constructor
        )

        # If our character is new and not loaded, give it default data
        if not loaded:
            self.create_default_content_data()  # Create data defaults for each chapter widget
            self.save_dict()    # Save our data to the file

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()


    # Called when creating new chapter widget, not when loading one
    def create_default_content_data(self) -> dict:
        ''' Returns default data all chapter widgets will have '''
        
        # Default data for new chapters
        default_chapter_data = {
            'content': "",    # Content of our chapter
        }

        # Update existing data with any new default fields we added
        self.data.update(default_chapter_data)  
        return
        
    
    def submit_mini_note(self, e):
        title = e.control.value
        self.create_mini_note(title)
        e.control.value = ""
        self.p.update()

    def create_mini_note(self, title: str):
        ''' Creates a mini note inside an image or chapter '''

        from models.mini_widgets.mini_note import MiniNote

        self.mini_widgets[title] = MiniNote(title=title, owner=self, page=self.p, data=None)

        self.reload_widget()


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        self.stack.controls.clear()

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

        print("Mini widgets in chapter:", self.mini_widgets)

        # Column that holds our mini note controls on the right 1/3 of the widget
        mini_notes_column = ft.Column(
            spacing=6,
            controls=self.mini_widgets.values(),   # They'll only be rendered if visible
        )

        for mini_widget in self.mini_widgets.values():
            if mini_widget.visible:
                mini_notes_column.expand = True
                break

        # Spacing container to give some space between our body and mini notes
        mini_notes_row = ft.Row(expand=True)

        # Create a spacinig container and add it so our mini notes only take up the right most 1/3 of widget
        spacing_container = ft.Container(expand=True, ignore_interactions=True)
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

        