import flet as ft
from models.user import user
from handlers.render_widgets import render_widgets

# An extended flet tab that every object in our story will derive from
# Has a title, tag, page reference, and pin location
class Widget(ft.Container):
    def __init__(self, title: str, tag: str, p: ft.Page, pin_location: str):
    # Variables that all widgets will have, so we'll store them outside of data
        self.title = title  # Name of character, but all objects have a 'title' for identification, so characters do too
        self.tag = tag  # Tag for logic, mostly for routing it through our story object
        self.p = p   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
        self.pin_location = pin_location  # Start in left pin location
        self.tab_color = ft.Colors.PRIMARY  # Since all objects are containers

        self.hide_tab_icon = ft.IconButton(    # Icon to hide the tab from the workspace area
            scale=0.8,
            on_click=lambda e: self.hide_widget(),
            icon=ft.Icons.CLOSE_ROUNDED,
            icon_color=ft.Colors.OUTLINE,
        )

        super().__init__(
            expand=True, 
            #padding=6,
            #border=ft.border.all(1, self.tab_color),  # Gives a border to match the widgets border
            #border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor=ft.Colors.ON_SECONDARY,
            #bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_SECONDARY),
            bgcolor=ft.Colors.TRANSPARENT,  # Makes it invisible
        )

    def hover_tab(self, e):
        self.hide_tab_icon.icon_color = ft.Colors.ON_PRIMARY_CONTAINER
        self.p.update()

    def stop_hover_tab(self, e):
        self.hide_tab_icon.icon_color = ft.Colors.OUTLINE
        self.p.update()

        

    # Makes our widget invisible
    def hide_widget(self):
        self.visible = False
        user.active_story.master_stack.update()
        render_widgets(self.p)

    # Shows our widget once again
    def show_widget(self):
        self.visible = True
        user.active_story.master_stack.update()
        render_widgets(self.p)
        self.p.update()
