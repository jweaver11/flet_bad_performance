import flet as ft
from models.user import user
from handlers.render_widgets import show_pin_drag_targets

story = user.active_story  # Get our story object from the user

# Class for each character. Requires passing in a name
class Character(ft.Container):
    def __init__(self, name, ):
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

        self.color = "none"     # Changable border color of widget and character on rail
        self.rendered_color = ft.Colors.TRANSPARENT   # Flet colors formatting based on our above color
        self.name_color = ft.Colors.PRIMARY     # flet color based on characters status of good, evil, neutral, or N/A


        # Data about the character that the user will manipulate
        # Can't call this 'data' since containers already have that property
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
            bgcolor = ft.Colors.GREY_900,
            content=None,
        )
        self.reload_widget() # Builds our widgets content when object is created
           
 
    # Makes our widget invisible
    def hide_widget(self):
        self.visible = False
        story.master_stack.update()

    # Called when the 'good' character option is clicked in the widget body
    def make_character_good(self):
        # Make sure our other 2 options are false, and good is true
        self.char_data['Good'] = True
        self.char_data['Evil'] = False
        self.char_data['Neutral'] = False
        self.check_morality()   # Changes the name_color variable based on our updated tags
        self.reload_widget()
        self.update()

    # Called when the 'evil' character option is clicked in the widget body
    def make_character_evil(self):
        self.char_data['Good'] = False
        self.char_data['Evil'] = True
        self.char_data['Neutral'] = False
        self.check_morality()
        self.reload_widget()
        self.update()

    # Called when the neutral character option is clicked in the widget body
    def make_character_neutral(self):
        self.char_data['Good'] = False
        self.char_data['Evil'] = False
        self.char_data['Neutral'] = True
        self.check_morality()
        self.reload_widget()
        self.update()

    # Called when the n/a character option is clicked in the widget body
    def make_character_na(self):
        self.char_data['Good'] = False
        self.char_data['Evil'] = False
        self.char_data['Neutral'] = False
        self.check_morality()
        self.reload_widget()
        self.update()
    
    # Called by the changes in characters morality. Changes the name_color property to reflect thos changes
    def check_morality(self):
        if self.char_data['Good'] == True:
            self.name_color = ft.Colors.GREEN
        elif self.char_data['Evil'] == True:
            self.name_color = ft.Colors.RED
        elif self.char_data['Neutral'] == True:
            self.name_color = ft.Colors.GREY
        else:
            self.name_color = ft.Colors.PRIMARY

    # Reloads/builds our widget. Called after any changes happen to the data in it
    def reload_widget(self):

        #self.controls.append(ft.Image(src=self.image, width=100, height=100))

        # Gives our container a border and adjusts the user selected color to it
        self.border = ft.border.all(2, self.rendered_color)

       
        self.content=ft.Column(spacing=0, controls=[
            ft.Stack([
                # Draggable title of character at top center of widget
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Draggable(
                            group="widgets",
                            content=ft.TextButton(content=ft.Text(weight=ft.FontWeight.BOLD, color=self.name_color, value=self.title)),
                            data=self,       # Pass our object as the data so we can access it
                            on_drag_start=show_pin_drag_targets,    # Called from rendered_widgets handler
                            # No on_complete method since the drag target will handle that
                            # If an on_cancel method gets added to flet, we add it here to remove the drag targets
                        )
                    ]
                ),
                # Hide widget eyeball button at top right of widget
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
                content=ft.Column([
                    ft.TextButton(text="good", on_click=lambda e: self.make_character_good()),
                    ft.TextButton(text="bad", on_click=lambda e: self.make_character_evil()),
                    ft.TextButton(text="neutral", on_click=lambda e: self.make_character_neutral()),
                    ft.TextButton(text="N/A", on_click=lambda e: self.make_character_na()),
                ])
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




# Make widget container contain markdown for rendereding, and scrollable

