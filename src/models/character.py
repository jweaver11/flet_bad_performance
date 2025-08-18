import flet as ft
from models.user import user
from models.widget import Widget
import os
import json


# Class for character objects in the story. Every object needs a title, and a page reference when created
class Character(Widget):
    def __init__(self, name, page: ft.Page):

        # Sets our Character as an extended Widget object, which is a subclass of a flet Container
        # Widget requires a title, tag, page reference, and a pin location
        super().__init__(
            title = name,  # Name of character, but all objects have a 'title' for identification, so characters do too
            tag = "character",  # Tag for logic, mostly for routing it through our story object
            p = page,   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
            pin_location = "left",  # Start in left pin location
        )

        #self.image = ""     # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False)
        
        self.name_color = ft.Colors.PRIMARY     # flet color based on characters status of good, evil, neutral, or N/A


        self.character_data = {
            'Role': "Main",     # Char is either main, side, or bg. Doesn't show up in widget, but user can still change it  
            'Morality': "",
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
                #on_change=self.sex_submit,
            ),
            #'Age': "0",   # Text field
            'Age': ft.TextField(
                label="Age",
                adaptive=True,      # Changes textfield depending on device (apple vs non-apple)
                capitalization=ft.TextCapitalization.SENTENCES, 
                width=80,
                #on_blur=self.age_change,        # Runs on either submission or click off
                #on_change=self.age_change      # This would run every keystroke
            ),
            'Physical Description': ft.Row(
                wrap=True,
                data={
                    'Race': "",
                    'Skin Color': "",
                    'Hair Color': "",   # Textfield
                    'Eye Color': "",    # Textfield
                    'Height': "",   # TextField
                    'Weight': "",   # TextField
                    'Build': "",    # 
                    'Distinguishing Features': "",  # some sort of flet list
                },
                controls=[
                    #ft.Container(ft.Text("Physical Description"), on_click=self.expand_physical_description),
                    ft.TextField(
                        label="Race",
                        adaptive=True,
                        capitalization=ft.TextCapitalization.SENTENCES, 
                        width=80,
                        #on_blur=self.race_change,   
                    ),
                ],
            ),
            'Family': ft.Row(     # Expandable
                wrap=True,
                data={     
                    #'Love Interest': Character or str,
                    'Love Interest': str,
                    'Father': "",   # Textfield with selectable options
                    'Mother': "",    
                    'Siblings': "",
                    'Children': "",
                    'Ancestors': "",
                },  
                controls=[
                    ft.Container(ft.TextButton("Family")),
                    ft.TextField(
                        label="Love Interest",
                        adaptive=True,
                        capitalization=ft.TextCapitalization.SENTENCES, 
                        width=320,
                        #on_blur=self.race_change,   
                    ),
                    ft.TextField(
                        label="Love Interest",
                        adaptive=True,
                        capitalization=ft.TextCapitalization.SENTENCES, 
                        width=120,
                        #on_blur=self.race_change,   
                    ),
                ]
            ),
            'Occupation': "",   # Textfield
            'Goals': "",    # Textfield list
            'Origin': {     # Category on the left
                'Birth Date': "",   # textfield
                'Hometown': "",     # Textfield and a select from location radio picker
                'Education': "",        # Textfield
            },
            
            'Personality': "",  # expandable ft.TextField
            'Backstory': "",    # expandable ft.TextField
            'Abilities': "",    # Some sort of list
            'Dead': [bool, "when they died"],
            'Notes' : [],   # Category that says Notes on the left, then lists the expandable ft.TextField
        }
        # Build our widget on start
        self.reload_widget()

    # Reloads/builds our widget. Called after any changes happen to the data in it
    def reload_widget(self):

        #self.controls.append(ft.Image(src=self.image, width=100, height=100))


        body = ft.Container(
            expand=True,
            padding=6,
            #bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.ON_SECONDARY),
            content=ft.Column([
                ft.Text("hi from " + self.title),
                ft.Dropdown(        # Dropdown selection of good, evil, neutral, and n/a
                    label="Morality",
                    value=self.character_data['Morality'],
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
            ])

        )

        self.tab.content=body

        # Sets our header
        tab = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
                 
        )
          
        
        # Set our content
        self.content = tab
                            #ft.Divider(color=self.tab_color, thickness=2),
                       
    
    # Change our tab color of widget. Accepts a flet color as parameter
    def change_color(self, color):
        self.tab_color = color
        self.reload_widget()
        self.p.update()

    
    # Called when the morality dropdown is changed
    # Sets our new morality based on the choice selected. Applies changes to name_color, the rail, and the widget
    def morality_change(self, e):
        print("Morality change ran")
        self.character_data['Morality'] = e.control.value

        self.check_morality(e)
        self.reload_widget()    # Apply our changes to the name at top of widget

        self.p.update()
    
    # Called by the changes in characters morality. Changes the name_color property to reflect those changes
    def check_morality(self, e):
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
            elif self.character_data['Morality'] == "N/A":
                self.name_color = ft.Colors.GREY_300
            elif self.character_data['Morality'] == "Deselect":    # Deselect all choices
                self.name_color = ft.Colors.PRIMARY
                self.character_data['Morality'] = None
                
            # Update our color
            e.control.color = self.name_color
            e.control.value = self.character_data['Morality']

        # If setting is turned off for char name colors, make all characters name_color the primary color scheme
        else:
            print("Color changing disabled, turning off all their colors")
            for character in user.active_story.characters:
                character.name_color = ft.Colors.PRIMARY
            # Apply our changes
            self.p.update()
            return

        # Reload the rail
        from ui.rails.character_rail import reload_character_rail
        reload_character_rail(self.p)


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

    # Called when the age is changed. Changes the age data
    def age_change(self, e):
        print("Age change ran")
        self.character_data['Age'].data = e.control.value
        print(self.character_data['Age'].data)

    # Called when the race is changed. Changes the race data
    def race_change(self, e):
        print("Race change ran")
        self.character_data['Physical Description'].data['Race'] = e.control.value
        print(self.character_data['Physical Description'].data['Race'])
        self.p.update()

    # Expand the tile to show physical descriptions
    def expand_physical_description(self, e):
        print("expand physical description ran")
            








'''
# Class for each character. Requires passing in a name
class Character(ft.Container):
    def __init__(self, name, page: ft.Page):
        # Variables that all widgets will have, so we'll store them outside of data
        self.title = name  # Name of character, but all objects have a 'title' for identification, so characters do too
        self.tag = "character"  # Tag for logic, mostly for routing it through our story object
        self.p = page   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
        self.pin_location = "left"  # Start in left pin location

        self.image = ""     # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False, col={'xs': 12, 'sm': 12, 'md': 3})

        self.color = ft.Colors.GREY_800   # User defined color of the widget of the character
        self.name_color = ft.Colors.PRIMARY     # flet color based on characters status of good, evil, neutral, or N/A
        
        # Data about the character that the user will manipulate
        # Can't call this 'data' since containers already have that property, and generally that data needs to be a string
        # Our data is stored as normal json...
        # or as flet controls, which have the values stored in the parameter called "data" within each control
        # Data inside of a flet control must be a simple data type, usually str, bool, or int. Complex ones are a pain to read, as shown when
        # Objects are passed through their own draggables to move pins around.
        # Example: print(self.character_data['Sex'].data) -> Male
        self.character_data = {
            'Role': "Main",     # Char is either main, side, or bg. Doesn't show up in widget, but user can still change it  
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
            #'Age': "0",   # Text field
            'Age': ft.TextField(
                label="Age",
                adaptive=True,      # Changes textfield depending on device (apple vs non-apple)
                capitalization=ft.TextCapitalization.SENTENCES, 
                width=80,
                on_blur=self.age_change,        # Runs on either submission or click off
                #on_change=self.age_change      # This would run every keystroke
            ),
            'Physical Description': ft.Row(
                wrap=True,
                data={
                    'Race': "",
                    'Skin Color': "",
                    'Hair Color': "",   # Textfield
                    'Eye Color': "",    # Textfield
                    'Height': "",   # TextField
                    'Weight': "",   # TextField
                    'Build': "",    # 
                    'Distinguishing Features': "",  # some sort of flet list
                },
                controls=[
                    ft.Container(ft.Text("Physical Description"), on_click=self.expand_physical_description),
                    ft.TextField(
                        label="Race",
                        adaptive=True,
                        capitalization=ft.TextCapitalization.SENTENCES, 
                        width=80,
                        on_blur=self.race_change,   
                    ),
                ],
            ),
            'Family': ft.Row(     # Expandable
                wrap=True,
                data={     
                    'Love Interest': Character or str,
                    'Father': "",   # Textfield with selectable options
                    'Mother': "",    
                    'Siblings': "",
                    'Children': "",
                    'Ancestors': "",
                },  
                controls=[
                    ft.Container(ft.TextButton("Family")),
                    ft.TextField(
                        label="Love Interest",
                        adaptive=True,
                        capitalization=ft.TextCapitalization.SENTENCES, 
                        width=320,
                        on_blur=self.race_change,   
                    ),
                    ft.TextField(
                        label="Love Interest",
                        adaptive=True,
                        capitalization=ft.TextCapitalization.SENTENCES, 
                        width=120,
                        on_blur=self.race_change,   
                    ),
                ]
            ),
            'Occupation': "",   # Textfield
            'Goals': "",    # Textfield list
            'Origin': {     # Category on the left
                'Birth Date': "",   # textfield
                'Hometown': "",     # Textfield and a select from location radio picker
                'Education': "",        # Textfield
            },
            
            'Personality': "",  # expandable ft.TextField
            'Backstory': "",    # expandable ft.TextField
            'Abilities': "",    # Some sort of list
            'Dead': [bool, "when they died"],
            'Notes' : [],   # Category that says Notes on the left, then lists the expandable ft.TextField
        }


        # Make a markdown as content of container
        # Gives us our initial widget as a container
        super().__init__(
            #expand=True, 
            #padding=6,
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

    def show_widget(self):
        self.visible = True
        user.active_story.master_stack.update()
        render_widgets(self.p)
        self.p.update()

    def change_color(self, color):
        self.color = color
        self.reload_widget()
        self.p.update()

    
    # Called when the morality dropdown is changed
    # Sets our new morality based on the choice selected. Applies changes to name_color, the rail, and the widget
    def morality_change(self, e):
        e.control.data = e.control.value

        self.check_morality()
        self.reload_widget()    # Apply our changes to the name at top of widget

        self.p.update()
    
    # Called by the changes in characters morality. Changes the name_color property to reflect thos changes
    def check_morality(self):
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

    # Called when the age is changed. Changes the age data
    def age_change(self, e):
        print("Age change ran")
        self.character_data['Age'].data = e.control.value
        print(self.character_data['Age'].data)

    # Called when the race is changed. Changes the race data
    def race_change(self, e):
        print("Race change ran")
        self.character_data['Physical Description'].data['Race'] = e.control.value
        print(self.character_data['Physical Description'].data['Race'])
        self.p.update()

    # Expand the tile to show physical descriptions
    def expand_physical_description(self, e):
        print("expand physical description ran")
        

    # Save this character to its pickle file
    def save_to_file(self):
        """Save the character to its pickle file"""
        try:
            # Use the story's save method to handle the actual saving
            user.active_story.save_object_to_file(self)
            print(f"Character '{self.title}' saved successfully")
        except Exception as e:
            print(f"Error saving character '{self.title}': {e}")

    # Reloads/builds our widget. Called after any changes happen to the data in it
    def reload_widget(self):

        #self.controls.append(ft.Image(src=self.image, width=100, height=100))

        #self.border = ft.border.all(0, ft.Colors.GREY_800)  # Gives our container a border and adjusts the user selected color to it
       
        self.content=ft.Column(spacing=0, controls=[
        
            # Draggable title of character at top center of widget
            ft.Container(
                border = ft.border.all(2, self.color),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Draggable(
                            group="widgets",
                            content=ft.TextButton(content=ft.Text(weight=ft.FontWeight.BOLD, size=20, color=self.name_color, value=self.title)),
                            data=self,       # Pass our object as the data so we can access it
                            on_drag_start=show_pin_drag_targets,    # Called from rendered_widgets handler
                            # No on_complete method since the drag target will handle that
                            # If an on_cancel method gets added to flet, we add it here to remove the drag targets
                        ),
                        ft.IconButton(
                            on_click=lambda e: self.hide_widget(),
                            icon=ft.Icons.VISIBILITY_OFF_ROUNDED
                        ),
                    ]
                ),
            ),
           # ft.Divider(color=ft.Colors.OUTLINE_VARIANT),


            # Body of our widget
            ft.Container(       # Body of the widget
                expand=True,
                padding=6,
                content=ft.Column(  # List our character data inside a column, use rows to format left to right

                    scroll=ft.ScrollMode.AUTO,  # Enable scrolling if it doesnt all fit
                    expand=True,
                    controls=[             
                        ft.Row(     # Top row that shows icon, morality, sex, age
                            wrap=True,  # Enable increasing rows height and putting items that dont fit into columns
                            # ^^ Keeps formatting nice when expanding and shrinking widget
                            expand=True,
                            controls=[
                                self.icon, 
                                # Color pallet picker to change the characters color of outline of widget
                                ft.PopupMenuButton(
                                    opacity=1,
                                    scale=1.4,
                                    tooltip="",
                                    icon=ft.Icons.COLOR_LENS,
                                    icon_color=ft.Colors.PRIMARY, 
                                    items=[
                                        #on_click=lambda e, char=character: change_character_color(char, page),
                                        ft.PopupMenuItem(
                                            text="Red",
                                            content=ft.Text("Red", color=ft.Colors.RED, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.RED)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Pink",
                                            content=ft.Text("Pink", color=ft.Colors.PINK, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.PINK)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Purple",
                                            content=ft.Text("Purple", color=ft.Colors.PURPLE, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.PURPLE)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Blue",
                                            content=ft.Text("Blue", color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.BLUE)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Cyan",
                                            content=ft.Text("Cyan", color=ft.Colors.CYAN, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.CYAN)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Teal",
                                            content=ft.Text("Teal", color=ft.Colors.TEAL, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.TEAL)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Green",
                                            content=ft.Text("Green", color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.GREEN)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Lime",
                                            content=ft.Text("Lime", color=ft.Colors.LIME, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.LIME)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Yellow",
                                            content=ft.Text("Yellow", color=ft.Colors.YELLOW, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.YELLOW)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Orange",
                                            content=ft.Text("Orange", color=ft.Colors.ORANGE, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.ORANGE)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Brown",
                                            content=ft.Text("Brown", color=ft.Colors.BROWN, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.BROWN)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Light Grey",
                                            content=ft.Text("Light Grey", color=ft.Colors.GREY_500, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.GREY_300)
                                        ),
                                        ft.PopupMenuItem(
                                            text="Grey",
                                            content=ft.Text("Grey", color=ft.Colors.GREY_700, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.GREY_800)
                                        ),
                                        ft.PopupMenuItem(
                                            text="None",
                                            content=ft.Text("None", color=ft.Colors.GREY_300, weight=ft.FontWeight.BOLD), 
                                            on_click=lambda e: self.change_color(ft.Colors.TRANSPARENT)
                                        ),
                                    ]
                                ),
                                self.character_data['Morality'],
                                self.character_data['Sex'],
                                self.character_data['Age'],
                            ]
                        ),

                        # Next row which shows the physical desciption. Expands when button clicked
                        self.character_data['Physical Description'], 

                        # Next row that shows family, which can expand right to left
                        self.character_data['Family'],
                    
                        
                        
                        
                    ]
                )
            )
        ])
'''


