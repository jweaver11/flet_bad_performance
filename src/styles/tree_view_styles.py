import flet as ft
from models.story import Story

# The expansion tile for the timelines and arcs on the timelines rail
class Tree_View_Expansion_Tile(ft.ExpansionTile):
    def __init__(self, title, controls=None, on_change=None, scale=None):
        super().__init__(
            title=ft.Text(title),
            text_color="primary",
            dense=True,
            tile_padding=None,
            controls_padding=ft.Padding(10, 0, 0, 0),
            maintain_state=True,
            initially_expanded=True,
            expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
            shape=ft.RoundedRectangleBorder(),
            #controls=controls if controls else [],
            controls=[ft.Container(height=6)],
            #on_change=on_change,
        )

        et = ft.ExpansionTile("temp")


# Class for items within a tree view on the rail
class Tree_View_Item(ft.GestureDetector):

    def __init__(
        self, 
        title: str,         # Title of this item
        story: Story,       # Story reference for mouse positions
        page: ft.Page,    # Page reference for overlay menu
        on_exit,

        spacing: int = None,       # Spacing around the item. This increments. NEEDED???   
    ):
        
        self.title = title
        self.story = story
        self.p = page

        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.PRIMARY,
            font_family="Consolas",

        )

        super().__init__(
            on_enter=self.handle_enter,
            on_exit=on_exit,
            on_secondary_tap=lambda e: self.open_menu(),
            content = ft.Text(value=title, style=self.text_style),
            mouse_cursor=ft.MouseCursor.CLICK
        )

    # Called when hovering mouse over a tree view item
    def handle_enter(self, e):
        print("Hovered over item: " + self.title)

    def open_menu(self):
            
        #print(f"Open menu at x={story.mouse_x}, y={story.mouse_y}")

        def close_menu(e):
            self.p.overlay.clear()
            self.p.update()
        
        menu = ft.Container(
            left=self.story.mouse_x,     # Positions the menu at the mouse location
            top=self.story.mouse_y,
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.ON_SECONDARY,
            padding=2,
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.TextButton("Option 1"),
                ft.TextButton("Option 2"),
                ft.TextButton("Option 3"),
            ]),
        )
        outside_detector = ft.GestureDetector(
            expand=True,
            on_tap=close_menu,
            on_secondary_tap=close_menu,
        )

        self.p.overlay.append(outside_detector)
        self.p.overlay.append(menu)
        
        self.p.update()



