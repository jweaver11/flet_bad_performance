import flet as ft
from models.user import user
from handlers.render_widgets import show_pin_drag_targets

story = user.active_story  # Get our story object from the user

# Class for each character. Requires passing in a name
class Character(ft.Container):
    def __init__(self, name):
        self.title = name  # Name of character, but all objects have a title for identification
        self.tag = "character"  # Tag for logic, mostly for routing it through our story object

        self.pin_location = "left"  # Start in main pin location

        self.tags = {   # adjectives about the character for easier identification
            'main_character': True,      
            'side_character' : True,     
            'background_character': True,     
            'good' : True,
            'evil' : False,
            'neutral' : False,
            #man : bool
            #woman : bool
            #alive : 
            'color': True,
        }

        # These 3 outside of data so they can render differently
        self.image = "" # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.age = ""
        self.sex = ""    # Add selecteble male, female, other - custom write in
        self.color = "grey"     # Changable bg color of widget and bg of character on rail

        self.char_data = {
            'Good': True,
            'Evil': False,
            'Neutral': False,
            'Family': {'Father': "", 'Mother': ""}, #'Siblings': [], 'Children': [], 'Spouse': [], 'Ancestors': []
            'Occupation': "",
            'Goals': "",
            'Origin': {
                'Birthplace': "",
                'Birth Date': "",
                'Hometown': "",
                'Education': "",
            },
            'Physical Description': {
                'Hair Color': "",
                'Eye Color': "",
                'Height': "",
                'Weight': "",
                'Build': "",
                'Distinguishing Features': "",
            },
            'Personality': "",
            'Backstory': "",
            'Abilities': "",
            'Notes' : "",
        }

        # Make a markdown as content of container
        # Gives us our initial widget as a container
        super().__init__(
            expand=True, 
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor=self.color, # Uniformed bg color of the widget
            content=None
        )
        self.build_widget() # Builds our widgets content when object is created
           
 
    # Makes our widget invisible
    def hide_widget(self):
        self.visible = False
        story.master_stack.update()

    def build_widget(self):
        # Sets our color when we build widget, or it would have to set on every UI element
        
        if self.color == "red":
            render_color = ft.Colors.RED_900
        elif self.color == "pink":
            render_color = ft.Colors.PINK_900
        elif self.color == "purple":
            render_color = ft.Colors.PURPLE_900
        elif self.color == "blue":
            render_color = ft.Colors.BLUE_900
        elif self.color == "cyan":
            render_color = ft.Colors.CYAN_900
        elif self.color == "teal":
            render_color = ft.Colors.TEAL_900
        elif self.color == "green":
            render_color = ft.Colors.GREEN_900
        elif self.color == "lime":
            render_color = ft.Colors.LIME_900
        elif self.color == "yellow":
            render_color = ft.Colors.YELLOW_900
        elif self.color == "orange":
            render_color = ft.Colors.ORANGE_900
        elif self.color == "brown":
            render_color = ft.Colors.BROWN_900
        elif self.color == "light_grey":
            render_color = ft.Colors.GREY_500
        elif self.color == "grey":
            render_color = ft.Colors.GREY_900
        else:
            render_color = ft.Colors.GREY_900

        #self.controls.append(ft.Image(src=self.image, width=100, height=100))
        self.bgcolor=render_color
       
        self.content=ft.Column(spacing=0, controls=[
            ft.Stack([
                # Draggable title of character at top center of widget
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Draggable(
                            group="widgets",
                            content=ft.TextButton(self.title),
                            data=self,       # Pass our object as the data so we can access it
                            on_drag_start=show_pin_drag_targets,    # Called from render_widgets handler
                            # No on_complete method since the drag target will handle that
                        )
                    ]
                ),
                # Hide widget 'x' button at top right of widget
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.IconButton(
                            on_click=lambda e: self.hide_widget(),
                            icon=ft.Icons.VISIBILITY_OFF_ROUNDED
                )])
            ]),
            # Divider between title and body of widget
            ft.Divider(color=ft.Colors.PRIMARY),

            # Body of our widget
            ft.Container(       # Body of the widget
                expand=True,
                content=ft.Column()
            )
        ])
    

    # origin = Origin

    # unique data types, (not str)
    #color : str
    icon : str

    # Add ons that won't show by default
    race: str
    species : str
    parents = []




# Make widget container contain markdown for rendering, and scrollable

