'''
An extended flet container that is the parent of all our story objects.
Handles uniform UI, and has some functionality all objects need for easy data use.
All objects contain a title, tag, page reference, pin location, tab color, and a file path
'''


import flet as ft
from models.user import user
from handlers.render_widgets import render_widgets
from handlers.render_widgets import show_pin_drag_targets


class Widget(ft.Container):
    def __init__(self, title: str, tag: str, p: ft.Page, pin_location: str, tab_color: str):
    
        self.title = title  # Title of our object
        self.tag = tag  # Tag for logic routing and identification
        self.p = p   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen...
        # p.update() always works - (self.update() and page.update() sometimes don't work because of outdated references)
        self.pin_location = pin_location  # Pin location of our object upon creation
        self.tab_color = tab_color  # Users can change the tab color of their widgets for better organization
        self.path = ""  # The path to the json file that stores this widget's data


        self.hide_tab_icon = ft.IconButton(    # Icon to hide the tab from the workspace area
            scale=0.8,
            on_click=lambda e: self.hide_widget(),
            icon=ft.Icons.CLOSE_ROUNDED,
            icon_color=ft.Colors.OUTLINE,
        )

        # Tab that holds our widget label and body.
        # This needs to be nested in a ft.Tabs control or it wont render.
        # We do this so we can use tabs in the main pin area, and user it as a container on the other pins
        self.tab = ft.Tab(
            content=ft.Container(), #Initialize the content
            tab_content=ft.Draggable(       # Keeps each tab draggable and uniform
                group="widgets",
                data=self,
                on_drag_start=show_pin_drag_targets,
                on_drag_complete=lambda e: print(f"Drag completed for {self.title}"),
                #on_drag_cancel=impliment when we have custom draggables
                content_feedback=ft.TextButton(self.title),
                content=ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.CLICK,
                    on_hover=self.hover_tab,
                    on_exit=self.stop_hover_tab,
                    #on_tap=self.on_tab_click,  # Add click handler for tab switching
                    content=ft.Row(
                        controls=[
                            ft.Container(width=6), # Padding we can still drag
                            ft.Text(
                                weight=ft.FontWeight.BOLD, 
                                color=self.tab_color, 
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                value=self.title, 
                                
                                #on_click=None,
                                #style=ft.ButtonStyle(
                                    #padding=ft.padding.only(left=6),
                                    #shadow_color="transparent",       # No shadow
                                    #overlay_color="transparent"       # No click effect/splash
                                #),
                                #text=self.title,
                            ),
                            self.hide_tab_icon,    # From the widget class
                        ]
                    )
                ),
            ),
                                
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

    def on_tab_click(self, e):
        """Handle tab click to switch to this tab"""
        # Find the parent Tabs control and set this tab as selected
        try:
            # Get the story object
            from models.user import user
            story = user.active_story
            
            # Find the tabs control in the main pin area
            visible_main_controls = [control for control in story.main_pin.controls if getattr(control, 'visible', True)]
            if len(visible_main_controls) > 1:
                # Find which tab index this widget corresponds to
                for i, control in enumerate(visible_main_controls):
                    if control == self:
                        # Find the tabs control and set the selected index
                        # We need to trigger a re-render to update the tabs
                        from handlers.render_widgets import render_widgets
                        
                        # Store the selected tab index in the story object
                        story.selected_main_tab_index = i
                        render_widgets(self.p)
                        break
        except Exception as ex:
            print(f"Error switching tab: {ex}")

        

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
