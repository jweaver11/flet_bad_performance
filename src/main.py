'''
The main file to run the application.
Initializes the user, settings, page data, and renders our UI onto the page
'''
# this is a test comment love cory
import flet as ft
from models.user import user
from handlers.routes import route_change
from models.settings import Settings
from ui.all_workspaces_rails import All_Workspaces_Rail
from ui.active_rail import Active_Rail
from ui.menu_bar import create_menu_bar
from handlers.reload_workspace import reload_workspace
from ui.workspace import create_workspace


# Main function
def main(page: ft.Page):
    
    #page.on_route_change = route_change

    # Checks if our user settings exist. This will only run if the user is newly created
    # Otherwise, when the user loads in, their settings will load as well
    if user.settings is None:
        # We create our user settings here because we need the page reference
        user.settings = Settings(page)  

    user.set_new_active_story()  # Sets our active story based on what is in settings

    print("num stories: ", len(user.stories))

    # Grabs our active story, and loads all our data into its objects for the program
    if user.active_story is not None:
        user.active_story.startup(page)

    # Adds our page title
    title = "StoryBoard -- " + "user.active_story.title" + " -- Saved status"

    # Sets our theme modes and color schemes based on user settings (first start is dark and blue)
    page.theme = ft.Theme(color_scheme_seed=user.settings.data['theme_color_scheme'])
    page.dark_theme = ft.Theme(color_scheme_seed=user.settings.data['theme_color_scheme'])
    page.theme_mode = user.settings.data['theme_mode']
   
    # Sets the title of our app, padding, and maximizes the window
    page.title = title
    page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
    page.window.maximized = True


    # Create our page elements as their own pages so they can update
    menubar = create_menu_bar(page)   

    # Create our rails inside of user so we can access it as an object and store preferences
    user.all_workspaces_rail = All_Workspaces_Rail(page)  # Create our all workspaces rail
    user.active_story.active_rail = Active_Rail(page)  # Container stored in story for the active rails


    # Create our workspace container to hold our widgets
    workspace = create_workspace()  # render our workspace containing our widgets


    # Called when hovering over resizer to right of the active rail
    def show_horizontal_cursor(e: ft.HoverEvent):
        ''' Changes the cursor to horizontal when hovering over the resizer '''

        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    # Called when resizing the active rail by dragging the resizer
    def move_active_rail_divider(e: ft.DragUpdateEvent):
        ''' Responsible for altering the width of the active rail '''

        if (e.delta_x > 0 and user.active_story.active_rail.width < page.width/2) or (e.delta_x < 0 and user.active_story.active_rail.width > 100):
            user.active_story.active_rail.width += e.delta_x    # Apply the change to our rail
            
        page.update()   # Apply our changes to the rest of the page

    # Called when user stops dragging the resizer to resize the active rail
    def save_active_rail_width(e: ft.DragEndEvent):
        ''' Saves our new width that will be loaded next time user opens the app '''

        user.settings.data['active_rail_width'] = user.active_story.active_rail.width
        user.settings.save_dict()
        print("Active rail width: " + str(user.active_story.active_rail.width))

    # The actual resizer for the active rail (gesture detector)
    active_rail_resizer = ft.GestureDetector(
        content=ft.Container(
            width=10,   # Total width of the GD, so its easier to find with mouse
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),  # Matches our bg color to the active_rail
            # Thin vertical divider, which is what the user will actually drag
            content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.OUTLINE_VARIANT),
            padding=ft.padding.only(left=8),  # Push the 2px divider ^ to the right side
        ),
        on_hover=show_horizontal_cursor,    # Change our cursor to horizontal when hovering over the resizer
        on_pan_update=move_active_rail_divider, # Resize the active rail as user is dragging
        on_pan_end=save_active_rail_width,  # Save the resize when user is done dragging
    )

    # Save our 2 rails, divers, and our workspace container in a row
    row = ft.Row(
        spacing=0,  # No space between elements
        expand=True,  # Makes sure it takes up the entire window/screen

        controls=[
            user.all_workspaces_rail,  # Main rail of all available workspaces
            ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

            user.active_story.active_rail,    # Rail for the selected workspace
            active_rail_resizer,   # Divider between rail and work area
            
            workspace,    # Work area for pagelets
        ],
    )

    # Format our page. Add our menubar at the top, then then our row built above
    col = ft.Column(
        spacing=0, 
        expand=True, 
        controls=[
            menubar, 
            row,
        ]
    )

    # Build our page we the column we created
    page.add(col)

    # Loads our widgets for the program whenever it starts. Make sure its called after page is built
    reload_workspace(page) 

    #page.views.pop()
    #page.views.append(user.active_story)


# Runs the app
ft.app(main)