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
        # Our data is stored as flet controls as well, and the values are stored in the parameter called "data" within each control
        # Example: print(self.character_data['Sex'].data) -> Male
        self.character_data = {
            'Role': "Main",     # Character is either main, side, or bg. 
            'Morality': "",     # Dropdown selection of good, evil, neutral, and n/a
            'Sex': ft.Dropdown(      # Dropdown of male and female, with button next to it to write in customs
                label="Sex",
                data="", 
                options=[
                    ft.DropdownOption(key="Male"),
                    ft.DropdownOption(key="Female"),
                ],
                on_change=self.sex_submit
            ),
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
            'Dead': [True, "when they died"],
            'Notes' : "",   # Category that says Notes on the left, then lists the expandable ft.TextField
        }

        # Icon button that shows the custom textfield when clicked
        #self.add_sex_icon = ft.IconButton(icon=ft.Icons.ADD_ROUNDED, on_click=self.show_custom_sex_textfield)
        #self.add_sex_icon = ft.IconButton(icon=ft.Icons.ADD_ROUNDED, on_click=self.show_custom_sex_textfield)
        # Textfield so user can input custom sex's
        #self.custom_sex_textfield = ft.TextField(label="Custom", width=100, visible=True, on_submit=self.submit_custom_sex)
        
        #self.custom_sex_textfield = ft.TextField(label="Custom", width=100, visible=True, on_submit=self.submit_custom_sex)

        #self.sex_options_dropdown = ft.Dropdown(
            #label="Sex",
            #value=self.character_data['Sex'],
            #on_change=self.sex_change,
           # on_blur=self.sex_change,    # Saves custom write ins
            #options=user.active_story.sex_options,
        #)

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

    # Pull our options for our morality dropdown
    def get_morality_options(e):
        morality_options = ["Good", "Evil", "Neutral", "N/a"]

        list = []
        for option in morality_options:   
            list.append(
                ft.DropdownOption(
                    text=option
                )
            )
        return list
    
    # Called when the morality dropdown is changed
    # Sets our new morality based on the choice selected. Applies changes to name_color, the rail, and the widget
    def morality_change(self, e):
        self.character_data['Morality'] = e.control.value
        self.check_morality()
        self.reload_widget()
        self.p.update()
    
    # Called by the changes in characters morality. Changes the name_color property to reflect thos changes
    def check_morality(self):
        # If we have the setting turned on to change char name colors, change them
        if user.settings.change_name_colors.value == True:
            print("color changing is true, we running the logic")
            # Check the morality and change color accordingly
            if self.character_data['Morality'] == "Good":
                self.name_color = ft.Colors.GREEN_200
            elif self.character_data['Morality'] == "Evil":
                self.name_color = ft.Colors.RED_200
            elif self.character_data['Morality'] == "Neutral":
                self.name_color = ft.Colors.GREY_300
            else:
                # If none are selected, make it color scheme
                self.name_color = ft.Colors.PRIMARY
        # If setting is turned off for char name colors, make all characters name_color the primary color scheme
        else:
            for char in user.active_story.characters:
                char.name_color = ft.Colors.PRIMARY
            # Apply our changes
            self.p.update()

            return print("Color changing disabled")
        # Reload the rail
        from workspaces.character.character_rail import reload_character_rail
        reload_character_rail(self.p)

    # Called when the textfield for writing in custom sex's is submitted
    # Adds our custom sex to our stories sex_options list
    def sex_submit(self, e):
        print(e.control.value)

        value = e.control.value

        # Save most of our variables in our data in the flet controls
        self.character_data['Sex'].data = e.control.value

        print("Data: ", self.character_data['Sex'].data)
        
        if value == "Male" or value == "Man" or value == "Boy" or value == "Guy":
            e.control.text_style = ft.TextStyle(color=ft.Colors.BLUE_ACCENT)
        elif value == "Woman" or value == "Female" or value == "Girl":
            e.control.text_style = ft.TextStyle(color=ft.Colors.PINK)
        else:
            e.control.text_style = ft.TextStyle(color=ft.Colors.PRIMARY)
        
        e.control.update()
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
                                ft.Dropdown(
                                    label="Morality",
                                    padding=ft.padding.all(0),
                                    color=self.name_color,
                                    value=self.character_data['Morality'],
                                    options=self.get_morality_options(),
                                    on_change=self.morality_change,
                                ),
                                self.character_data['Sex'],
                            ]
                        ),
                        ft.Row(
                            expand=True,
                            spacing=0,
                            controls=[
                                #self.sex_options_dropdown,
                                
                                #self.add_sex_icon,
                            ]
                        ),

                    
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

