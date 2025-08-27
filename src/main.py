'''
The main file to run the application.
Initializes the app, settings, page data, and renders our UI onto the page
'''
# this is a test comment love cory
import flet as ft
from models.app import app
from handlers.route_change import route_change
from constants.init import init_settings, init_load_saved_stories, init_set_route
from models.settings import Settings
from ui.all_workspaces_rails import All_Workspaces_Rail
from ui.active_rail import Active_Rail
from ui.menu_bar import create_menu_bar
from handlers.reload_workspace import reload_workspace
from ui.workspace import create_workspace



# Main function
def main(page: ft.Page):

    # Declare our global variables
    #global stories
    
    # Initializes our settings, stories, and sets our initial route, which manages our views
    init_settings(page)
    init_load_saved_stories(page)
    init_set_route(page)


    # Load our story view if there is an active story
    if page.route != "/":
        page.go(page.route)
        page.views.clear()
        
        page.views.append(app.stories[app.settings.data['active_story']])
        print("Setting to active story: ", app.settings.data['active_story'])
        page.update()
    else:
        if len(app.stories) == 0:
            page.add(create_page_if_no_stories_exist())
            print("No stories exist")
        else:
            page.add(create_page_if_no_stories_active())
            print("Stories exist, but no active story")



    # Otherwise, let main load a blank view with a large button to create first story




    # Grabs our active story, and loads all our data into its objects for the program
    #if app.active_story is not None:
        #app.active_story.startup(page)

    # Adds our page title
    # If settings.active_story is not None:
    #     page_title = "StoryBoard -- " + settings.active_story.title + " -- Saved status"
    # else:
    #     page_title = "StoryBoard"
    #page_title = "StoryBoard -- " + app.settings.data['active_story'] + " -- Saved status"

    # Sets our theme modes and color schemes based on app settings (first start is dark and blue)
    page.theme = ft.Theme(color_scheme_seed=app.settings.data['theme_color_scheme'])
    page.dark_theme = ft.Theme(color_scheme_seed=app.settings.data['theme_color_scheme'])
    page.theme_mode = app.settings.data['theme_mode']
   
    # Sets the title of our app, padding, and maximizes the window
    page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
    page.window.maximized = True


    # Create our page elements as their own pages so they can update
    menubar = create_menu_bar(page)   

    # Create our rails inside of app so we can access it as an object and store preferences
    all_workspaces_rail = All_Workspaces_Rail(page)  # Create our all workspaces rail
    #app.active_story.active_rail = Active_Rail(page)  # Container stored in story for the active rails


    # Create our workspace container to hold our widgets
    workspace = create_workspace()  # render our workspace containing our widgets

    # Called to create the page view if no stories exist
    def create_page_if_no_stories_exist() -> ft.Control:
        ''' Gives us the menubar, initial rail, and large buttons to create your first story'''

        page.title = "StoryBoard"
        page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
        
        menubar = create_menu_bar(page)   


        # Create our rails inside of app so we can access it as an object and store preferences
        all_workspaces_rail = All_Workspaces_Rail(page)  # Create our all workspaces rail
        active_rail = Active_Rail(page)  # Container stored in story for the active rails

        # Create our workspace container to hold our widgets
        workspace = create_workspace()  # render our workspace containing our widgets 
        #workspace.alignment = ft.MainAxisAlignment.CENTER

        # Save our 2 rails, divers, and our workspace container in a row
        row = ft.Row(
            spacing=0,  # No space between elements
            expand=True,  # Makes sure it takes up the entire window/screen

            controls=[
                all_workspaces_rail,  # Main rail of all available workspaces
                ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

                active_rail,    # Rail for the selected workspace
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
        
        return page.add(col)

    # Called if there is no active story, but stories do exist
    def create_page_if_no_stories_active() -> ft.Control:
        ''' Creates our page view with a menubar, all_workspaces_rail, and two large buttons for create and open story'''

        page.title = "StoryBoard"
        page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
        
        menubar = create_menu_bar(page)   

        # Create our rails inside of app so we can access it as an object and store preferences
        all_workspaces_rail = All_Workspaces_Rail(page)  # Create our all workspaces rail
        active_rail = Active_Rail(page)  # Container stored in story for the active rails

        # Create our workspace container to hold our widgets
        workspace = create_workspace()  # render our workspace containing our widgets 

        # Save our 2 rails, divers, and our workspace container in a row
        row = ft.Row(
            spacing=0,  # No space between elements
            expand=True,  # Makes sure it takes up the entire window/screen

            controls=[
                all_workspaces_rail,  # Main rail of all available workspaces
                ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

                active_rail,    # Rail for the selected workspace
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
        
        return page.add(col)


    # Called when hovering over resizer to right of the active rail
    def show_horizontal_cursor(e: ft.HoverEvent):
        ''' Changes the cursor to horizontal when hovering over the resizer '''

        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    # Called when resizing the active rail by dragging the resizer
    def move_active_rail_divider(e: ft.DragUpdateEvent):
        ''' Responsible for altering the width of the active rail '''

        if (e.delta_x > 0 and app.active_story.active_rail.width < page.width/2) or (e.delta_x < 0 and app.active_story.active_rail.width > 100):
            app.active_story.active_rail.width += e.delta_x    # Apply the change to our rail
            
        page.update()   # Apply our changes to the rest of the page

    # Called when app stops dragging the resizer to resize the active rail
    def save_active_rail_width(e: ft.DragEndEvent):
        ''' Saves our new width that will be loaded next time app opens the app '''

        app.settings.data['active_rail_width'] = app.active_story.active_rail.width
        app.settings.save_dict()
        print("Active rail width: " + str(app.active_story.active_rail.width))

    # The actual resizer for the active rail (gesture detector)
    active_rail_resizer = ft.GestureDetector(
        content=ft.Container(
            width=10,   # Total width of the GD, so its easier to find with mouse
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),  # Matches our bg color to the active_rail
            # Thin vertical divider, which is what the app will actually drag
            content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.OUTLINE_VARIANT),
            padding=ft.padding.only(left=8),  # Push the 2px divider ^ to the right side
        ),
        on_hover=show_horizontal_cursor,    # Change our cursor to horizontal when hovering over the resizer
        on_pan_update=move_active_rail_divider, # Resize the active rail as app is dragging
        on_pan_end=save_active_rail_width,  # Save the resize when app is done dragging
    )

    # Save our 2 rails, divers, and our workspace container in a row
    row = ft.Row(
        spacing=0,  # No space between elements
        expand=True,  # Makes sure it takes up the entire window/screen

        controls=[
            all_workspaces_rail,  # Main rail of all available workspaces
            ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

            app.active_story.active_rail,    # Rail for the selected workspace
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
    #page.add(col)
    #create_page_if_no_stories_active()

    #if app.active_story is not None:
        #page.go(app.active_story.route)  # Goes to our active story route if it exists
        #page.views.append(app.active_story)  # Adds our active story as a view so we can go back to it
    #else:
        #page.add(col)

    # Loads our widgets for the program whenever it starts. Make sure its called after page is built
    reload_workspace(page) 

    #page.views.pop()
    #page.views.append(app.active_story)


# Runs the app
ft.app(main)