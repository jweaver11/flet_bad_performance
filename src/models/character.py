import flet as ft
from models.user import user
from handlers.render_widgets import show_pin_drag_targets, render_widgets

story = user.active_story  # Get our story object from the user

# Class for each character. Requires passing in a name
class Character(ft.Container):
    def __init__(self, name, page: ft.Page):
        self.title = name  # Name of character, but all objects have a title for identification
        self.tag = "character"  # Tag for logic, mostly for routing it through our story object
        self.p = page   # Grab our page correctly, as sometimes the container doesn't load it correctly
        # with all the UI changes that happen

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
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False, col=3)
        

        self.color = ft.Colors.GREY_800   # User defined color of the widget of the character
        self.name_color = ft.Colors.PRIMARY     # flet color based on characters status of good, evil, neutral, or N/A
        


        # Data about the character that the user will manipulate
        # Can't call this 'data' since containers already have that property
        self.character_data = {
            'Morality': "good",     # Radio selection of good, evil, neutral, or none selected is N/A
            'Sex': "male",      # Radio with custom write in option
            'Age': "0",   # Text field
            'Family': {     #'Siblings': [], 'Children': [], 'Spouse': [], 'Ancestors': []
                'Father': "",   # Textfield with selectable options
                'Mother': ""    # Textfield with selectable options
            },   
            'Occupation': "",   # Textfield
            'Goals': "",    # Textfield list
            'Origin': {     # Category on the left
                'Birth Date': "",   # textfield
                'Hometown': "",     # Textfield and a select from location radio picker
                'Education': "",        # Textfield
            },
            'Physical Description': {
                'Hair Color': "",   # Textfield
                'Eye Color': "",    # Textfield
                'Height': "",   # TextField
                'Weight': "",   # TextField
                'Build': "",    # Expandable textfield
                'Distinguishing Features': "",  # some sort of flet list
            },
            'Personality': "",  # expandable ft.TextField
            'Backstory': "",    # expandable ft.TextField
            'Abilities': "",    # Some sort of list
            'Notes' : "",   # Category that says Notes on the left, then lists the expandable ft.TextField
        }

        # Make a markdown as content of container
        # Gives us our initial widget as a container
        super().__init__(
            expand=True, 
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor = user.settings.workspace_bgcolor,
            content=None,
        )
        self.reload_widget() # Builds our widgets content when object is created
           
 
    # Makes our widget invisible
    def hide_widget(self):
        self.visible = False
        story.master_stack.update()
        render_widgets(self.p)

    # Called when the 'good' character option is clicked in the widget body
    def make_character_good(self):
        # Changes our morality
        self.character_data['Morality'] = "good"
        self.check_morality()   # Changes the name_color variable based on our updated tags
        self.reload_widget()

        # Import and reload the rail. We import this dynamically to avoid circular imports
        # Try to avoid this when we can, but its a pretty limited use case, so we do it this way here
        from workspaces.character.character_rail import reload_character_rail
        reload_character_rail(self.p)

    # Called when the 'evil' character option is clicked in the widget body
    def make_character_evil(self):
        self.character_data['Morality'] = "evil"
        self.check_morality()
        self.reload_widget()

        from workspaces.character.character_rail import reload_character_rail
        reload_character_rail(self.p)

    # Called when the neutral character option is clicked in the widget body
    def make_character_neutral(self):
        self.character_data['Morality'] = "neutral"
        self.check_morality()
        self.reload_widget()

        from workspaces.character.character_rail import reload_character_rail
        reload_character_rail(self.p)

    # Called when the n/a character option is clicked in the widget body
    def make_character_na(self):
        self.character_data['Moraily'] = "n/a"
        
        self.check_morality()
        self.reload_widget()

        from workspaces.character.character_rail import reload_character_rail
        reload_character_rail(self.p)
    
    # Called by the changes in characters morality. Changes the name_color property to reflect thos changes
    def check_morality(self):
        # If we have the setting turned on to change char name colors, change them
        if user.settings.change_name_colors.value == True:
            print("color changing is true, we running the logic")
            # Check the morality and change color accordingly
            if self.character_data['Morality'] == "good":
                self.name_color = ft.Colors.GREEN_200
            elif self.character_data['Morality'] == "evil":
                self.name_color = ft.Colors.RED_200
            elif self.character_data['Morality'] == "neutral":
                self.name_color = ft.Colors.GREY_300
            else:
                # If none are selected, make it color scheme
                self.name_color = ft.Colors.PRIMARY
        # If setting is turned off for char name colors, make all characters name_color the primary color scheme
        else:
            for char in story.characters:
                char.name_color = ft.Colors.PRIMARY
            # Apply our changes
            self.p.update()

            return print("Color changing disabled")
        # Reload the rail
        from workspaces.character.character_rail import reload_character_rail
        reload_character_rail(self.p)

    # Reloads/builds our widget. Called after any changes happen to the data in it
    def reload_widget(self):

        #self.controls.append(ft.Image(src=self.image, width=100, height=100))

        self.border = ft.border.all(2, self.color)  # Gives our container a border and adjusts the user selected color to it
       
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
            ft.Divider(color=self.color),

            # Body of our widget
            ft.Container(       # Body of the widget
                expand=True,
                content=ft.Column(
                    
                    #col={"xs": 12, "md": 6, "lg": 3, "xl": 1, "xxl": 1},  # The 'col' property changes how many controls...
                    # will fit in a row based on each screen size. The "xs", "md", etc measure the parent container size in width
                    # If a col=12, it will be the only control on that row,
                    # If col=1, there will be 12 controls on that row
                    # If col=6, it will take up half of that row,
                    # If col=9 would take up 3/4 the row
                    # If col=3 it would take up 1/4 that row

                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    controls=[             

                        ft.ResponsiveRow(
                            #wrap=True, 
                            expand=True,
                            controls=[
                                self.icon, 

                                ft.Column([
                                ft.RadioGroup(
                                    content=ft.Row(
                                        col=9,
                                        expand=True,
                                        controls=[
                                            ft.Radio(label="Good", value="good", toggleable=True),
                                            ft.Radio(label="Evil", value="evil", toggleable=True),
                                            ft.Radio(label="Neutral", value="neutral", toggleable=True),
                                        ]
                                    )
                                ),
                                ft.RadioGroup(
                                    content=ft.Row(
                                        expand=True,
                                        controls=[
                                            ft.Radio(label="Man", value="man", toggleable=True),
                                            ft.Radio(label="Woman", value="woman", toggleable=True),
                                            ft.Radio(label="Other", value="other", toggleable=True),    # make writein
                                    ])
                                )
                                ]),

                                
                            ]
                        ),
                        ft.TextButton(text="good", width=100, on_click=lambda e: self.make_character_good()),
                        ft.TextButton(text="evil", width=100, on_click=lambda e: self.make_character_evil()),

                        ft.TextButton(text="neutral", width=100, on_click=lambda e: self.make_character_neutral()),
                        ft.TextButton(text="N/A", width=100, on_click=lambda e: self.make_character_na()),

                    
                    ]
                )
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

