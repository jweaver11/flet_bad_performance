import flet as ft
from models.user import user
from handlers.render_widgets import show_pin_drag_targets, render_widgets

#story = user.active_story  # Get our story object from the user

# Class for each character. Requires passing in a name
class Character(ft.Container):
    def __init__(self, name, page: ft.Page):
        self.title = name  # Name of character, but all objects have a title for identification
        self.tag = "character"  # Tag for logic, mostly for routing it through our story object
        self.p = page   # Grab our page correctly, as sometimes the container doesn't load it correctly
        # with all the UI changes that happen

        self.pin_location = "left"  # Start in left pin location

        self.image = ""     # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False, col={'xs': 12, 'sm': 12, 'md': 3})

        self.color = ft.Colors.GREY_800   # User defined color of the widget of the character
        self.name_color = ft.Colors.PRIMARY     # flet color based on characters status of good, evil, neutral, or N/A
        

        # Data about the character that the user will manipulate
        # Can't call this 'data' since containers already have that property
        # Our data is stored as normal json, or as flet controls as well, and the values are stored in the parameter called "data" within each control
        # Example: print(self.character_data['Sex'].data) -> Male
        self.character_data = {
            'Role': "Main",     # Character is either main, side, or bg. Not its own control because it does not show up on screen    
            'Morality': ft.Dropdown(        # Dropdown selection of good, evil, neutral, and n/a
                label="Morality",
                padding=ft.padding.all(0),
                color=self.name_color,
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                options=[
                    ft.DropdownOption(text="Good"),
                    ft.DropdownOption(text="Evil"),
                    ft.DropdownOption(text="Neutral"),
                    ft.DropdownOption(text="N/A"),
                    ft.DropdownOption(text="Deselect"),
                ],
                on_change=self.morality_change,
            ),
            'Sex': ft.Dropdown(      # Sex of each character
                label="Sex",
                padding=ft.padding.all(0),
                color=self.name_color,
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                options=[
                    ft.DropdownOption(text="Male"),
                    ft.DropdownOption(text="Female"),
                    ft.DropdownOption(text="Deselect"),
                ],
                on_change=self.sex_submit,
            ),
            'Age': "0",   # Text field
            'Race': "",
            'Skin Color': "",
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
            'Dead': [True, "when they died"],
            'Notes' : "",   # Category that says Notes on the left, then lists the expandable ft.TextField

        }


        # Make a markdown as content of container
        # Gives us our initial widget as a container
        super().__init__(
            expand=True, 
            padding=6,
            #border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor = user.settings.workspace_bgcolor,
            content=None,
        )
        self.reload_widget() # Builds our widgets content when object is created

    
    # Makes our widget invisible
    def hide_widget(self):
        self.visible = False
        user.active_story.master_stack.update()
        render_widgets(self.p)

    
    # Called when the morality dropdown is changed
    # Sets our new morality based on the choice selected. Applies changes to name_color, the rail, and the widget
    def morality_change(self, e):
        e.control.data = e.control.value
    
        # Called by the changes in characters morality. Changes the name_color property to reflect thos changes
        def check_morality():
            # If we have the setting turned on to change char name colors, change them
            if user.settings.change_name_colors.value == True:
                print("color changing is true, we running the logic")
                # Check the morality and change color accordingly
                if self.character_data['Morality'].data == "Good":
                    self.name_color = ft.Colors.GREEN_200
                elif self.character_data['Morality'].data == "Evil":
                    self.name_color = ft.Colors.RED_200
                elif self.character_data['Morality'].data == "Neutral":
                    self.name_color = ft.Colors.GREY_300
                elif self.character_data['Morality'].data == "N/A":
                    self.name_color = ft.Colors.GREY_300
                elif self.character_data['Morality'].data == "Deselect":    # Deselect all choices
                    self.name_color = ft.Colors.PRIMARY
                    self.character_data['Morality'].value = None
                    
                # Update our color
                self.character_data['Morality'].color = self.name_color

            # If setting is turned off for char name colors, make all characters name_color the primary color scheme
            else:
                print("Color changing disabled, turning off all their colors")
                for character in user.active_story.characters:
                    character.name_color = ft.Colors.PRIMARY
                # Apply our changes
                self.p.update()
                return

            # Reload the rail
            from workspaces.character.character_rail import reload_character_rail
            reload_character_rail(self.p)

        check_morality()
        self.reload_widget()

        self.p.update()

    # Called when the textfield for writing in custom sex's is submitted
    # Adds our custom sex to our stories sex_options list
    def sex_submit(self, e):
        print("Color change ran")

        # Save most of our variables in our data in the flet controls
        e.control.data = e.control.value

        # If deselect is clicked
        if self.character_data['Sex'].data == "Deselect":
            self.character_data['Sex'].value = None
            self.reload_widget()    # When manually resetting value, must reload widget
        
        # If deselect is not clicked
        elif self.character_data['Sex'].data == "Male":
        # Checks that our data saved correctly, and changes color accordingly
            self.character_data['Sex'].color = ft.Colors.BLUE
            
        elif self.character_data['Sex'].data == "Female":
            self.character_data['Sex'].color = ft.Colors.PINK
        
        self.p.update()

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
                        ft.Row(
                            wrap=True, 
                            expand=True,
                            controls=[
                                self.icon, 
                                self.character_data['Morality'],
                                self.character_data['Sex'],
                            ]
                        ),
                    
                    ]
                )
            )
        ])
    



