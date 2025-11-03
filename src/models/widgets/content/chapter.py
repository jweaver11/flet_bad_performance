import flet as ft
from models.story import Story
from models.widget import Widget
from handlers.verify_data import verify_data


# Class that holds our text chapter objects
class Chapter(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):

        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  
            page = page,  
            directory_path = directory_path,  
            story = story,       
            data = data,    
        )

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            object=self,   # Pass in our own data so the function can see the actual data we loaded
            required_data={
                'tag': "chapter",
                'summary': str,     # Summary of what will happen in the chapter
                'content': str,
                'temp': str,
                'test': str,
                'mini_notes': dict,
            }
        )

        self.mini_notes = {}
        self.load_mini_notes()

        # Load our widget UI on start after we have loaded our data
        self.reload_tab()
        self.reload_widget()


    def load_mini_notes(self):
        ''' Loads our mini notes from our data into live objects '''
        from models.mini_widgets.mini_note import MiniNote

        # Loop through our data mini notes and create live objects for each
        for note_title, note_data in self.data['mini_notes'].items():
            self.mini_widgets.append(MiniNote(
                title=note_title,
                owner=self,
                father=self,
                page=self.p,
                dictionary_path="mini_notes",
                data=note_data,
            ))
    
    def submit_mini_note(self, e):
        title = e.control.value
        self.create_mini_note(title)
        e.control.value = ""
        self.reload_widget()


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''


        # BUILDING BODY - the inside the body container of our widget
        self.body_container.content = ft.Column(
            expand=True,
            controls=[
                ft.Text(f"hello from: {self.title}"),
                ft.TextField(
                    label="Create Mini Note",
                    hint_text="Mini Note Title",
                    expand=True,
                    on_submit=self.submit_mini_note,
                )
            ]
        )

        self._render_widget()

        