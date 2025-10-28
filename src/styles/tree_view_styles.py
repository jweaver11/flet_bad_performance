import flet as ft
from models.story import Story

# Expansion tile for all sub directories (folders) in a directory
class Tree_View_Directory(ft.GestureDetector):

    def __init__(self, 
        title: str,         # Title of this item
        story: Story,       # Story reference for mouse positions
        page: ft.Page,      # Page reference for overlay menu
        color: str = None,
        father: 'Tree_View_Directory' = None,
    ):
        
        self.title = title
        self.story = story
        self.p = page
        self.father = father
        self.color = color

        print(f"Color inside of tree view directory {title}:", color)


        self.expansion_tile = ft.ExpansionTile(
            title=ft.Text(value=title, weight=ft.FontWeight.BOLD, text_align="left"),
            #text_color="primary",
            dense=True,
            tile_padding=ft.Padding(0, 0, 0, 0),
            controls_padding=ft.Padding(10, 0, 0, 0),
            leading=ft.Icon(ft.Icons.FOLDER_OPEN, color=color if color is not None else "primary"),
            maintain_state=True,
            expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
            #shape=ft.RoundedRectangleBorder(),
            #controls=[ft.Container(height=6)],
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(),
        )

        super().__init__(
            mouse_cursor=ft.MouseCursor.CLICK,
            #on_enter=self.on_hover,
            on_exit=self.on_stop_hover,
            content = self.expansion_tile,
        )

    def on_hover(self, e):
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
        if self.father is not None:
            self.father.content.bgcolor = ft.Colors.TRANSPARENT
        self.p.update()
       

    def on_stop_hover(self, e):
        self.bgcolor = ft.Colors.TRANSPARENT
        self.p.update()
        


# Class for items within a tree view on the rail
class Tree_View_File(ft.GestureDetector):

    def __init__(
        self, 
        title: str,         # Title of this item
        story: Story,       # Story reference for mouse positions
        page: ft.Page,      # Page reference for overlay menu
        on_exit,
        tag: str = None,    # Optional tag to pass in for file type identification, so we can change icon 
        father: Tree_View_Directory = None,   

    ):
        
        self.title = title
        self.story = story
        self.p = page
        self.father = father

        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.PRIMARY,
            #font_family="Consolas",
            weight=ft.FontWeight.BOLD,
        )

        super().__init__(
            on_enter = self.on_hover,
            on_exit = self.on_stop_hover,
            on_secondary_tap = self.open_menu,
            content = ft.Container(expand=True, content=ft.Row([ft.Icon(ft.Icons.STICKY_NOTE_2_OUTLINED, color="primary"), ft.Text(value=title, style=self.text_style)], expand=True)),
            mouse_cursor = ft.MouseCursor.CLICK
        )

    # Called when hovering mouse over a tree view item
    def on_hover(self, e):
        self.content.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
        self.p.update()

    def on_stop_hover(self, e):
        self.content.bgcolor = ft.Colors.TRANSPARENT
        self.p.update()

    def open_menu(self, e):
            
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



