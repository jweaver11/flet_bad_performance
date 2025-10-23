import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data
from models.widgets.timeline import Timeline


# Display that makes timelines share much uniformaty in their information display like arcs do
class Timeline_Information_Display(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father: Timeline, page: ft.Page, dictionary_path: str, data: dict=None):

        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,        
            father=father,      # In this case, father is always the timeline we belong to
            page=page,          
            dictionary_path=dictionary_path,  # Not used, but its required so just whatever works
            data=None,      # We reference our owner data only. NEVER REFERENCE THIS DATA
        ) 
        
        # Since we mirror our timelines data, we don't need to verify it here

        self.reload_mini_widget()

    # Called when saving changes to our timeline object
    def save_dict(self):
        ''' Overwrites standard mini widget save and save our timelines data instead '''
        try:
            self.owner.save_dict()
        except Exception as e:
            print(f"Error saving timeline information display data to {self.owner.title}: {e}")

    # Called when reloading our mini widget UI
    def reload_mini_widget(self):

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
            ],
            expand=True,
        )

        self.p.update()