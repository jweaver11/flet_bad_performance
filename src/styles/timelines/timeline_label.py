import flet as ft
from models.widgets.timeline import Timeline
from models.story import Story
from styles.menu_option_style import Menu_Option_Style


# Class for labels of plot points and arcs used underneath timeline drops and arc drop downs
class Timeline_Label(ft.GestureDetector):
    def __init__(
        self, 
        title: str,
        icon: ft.Icon,
        story: Story,
        father: Timeline,            # Father timeline or arc object to create new items
    ):

        self.title = title
        self.icon = icon
        self.story = story

        super().__init__(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_items()),
        )

        self.reload()


    def get_menu_items(self) -> list[ft.Control]:
        ''' Returns a list of menu items when right clicking this label '''

        # Option for either plot point or arcs
        return [
            Menu_Option_Style(
                #on_click=self.rename_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED),
                    ft.Text(
                        "Rename", 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.ON_SURFACE
                    ), 
                ]),
            )
        ]


    def reload(self):
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                #ft.Icon(self.icon, color=ft.Colors.PRIMARY, size=16),
                ft.Text(self.title, weight=ft.FontWeight.BOLD),
            ],
        )
    



            

    