import flet as ft
from models.mini_widget import Mini_Widget
from models.widget import Widget
from models.widgets.timeline import Timeline


# Display that makes timelines share much uniformaty in their information display like arcs do
class Timeline_Information_Display(Mini_Widget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father: Timeline, page: ft.Page, key: str, data: dict=None):

        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,                    
            father=father,                  # In this case, father is always the timeline or arc we belong to
            page=page,          
            key=key,  # Not used, but its required so just whatever works
            data=None,      # No data is used here, so NEVER reference it. Use self.owner.data instead
        ) 
        
        # Since we only reference out owners data and not our own, we don't need to verify it here

        # Set our visibility based on our owners data
        self.visible = self.owner.data['information_display']['visibility']

        self.reload_mini_widget()

    # Called when saving changes to our timeline object
    def save_dict(self):
        ''' Overwrites standard mini widget save and save our timelines data instead '''
        try:
            self.owner.save_dict()
        except Exception as e:
            print(f"Error saving timeline information display data to {self.owner.title}: {e}")

    # Called when toggling our visibility
    def toggle_visibility(self, e=None, value: bool=None, not_active: bool=False):
        ''' Custom toggles our visibility for our information display '''

        if value is not None:
            self.visible = value
            self.owner.data['information_display']['visibility'] = value

        else:

            # Update our visibility (stored in owners data)
            self.owner.data['information_display']['visibility'] = not self.owner.data['information_display']['visibility']
            self.visible = self.owner.data['information_display']['visibility']
            
        # Save switch to file
        self.save_dict()

        if not_active:
            pass
        else:
            self.owner.set_active_mini_widget(self)

        print(f"Toggling visibility of mini widget {self.title}. We are visible: {self.visible}")
        

    # Called when reloading our mini widget UI
    def reload_mini_widget(self):

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,

                ft.TextButton("Hide me", on_click=self.toggle_visibility),
            ],
            expand=True,
        )

        self.p.update()