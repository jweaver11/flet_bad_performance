'''
Most model classes really container 2 models: the character model itself and the associated widget model.
Inside of the 'data' dict, we store our characters model for the manipulative data...
the app will change. Everything else is built upon program launch so we can display it in the UI.
'''

import flet as ft
import json
import os
from models.app import app
from models.widget import Widget
from models.story import Story


# Sets our Character as an extended Widget object, which is a subclass of a flet Container
# Widget requires a title, tag, page reference, and a pin location
class Character(Widget):
    # Constructor
    def __init__(self, name: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):

        # Parent class constructor
        super().__init__(
            title = name,  # Name of character, but all objects have a 'title' for identification, so characters do too
            tag = "character",  # Tag for logic, for routing and for import/export
            p = page,   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
            directory_path = directory_path,    # Directory where our json file is stored
            story = story,   # Grabs our story reference so we can access story data and save our character in the right folder
            data = data,
        )

        # If no data passed in (New character, not loaded one), give it default data
        if self.data is None:
            self.data = self.create_default_data()
            self.save_dict()    # Save our data to the file if the character is new

        
        self.visible = self.data['visible']  # Whether or not this character is visible in the character rail
        
        

        # Variables that have to be loaded differently from data
        #self.image = ""     # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False)    # Icon of character

        # Load our character data from the file, or set default data if creating new character

        # if data is None, create default data() -> default data

        # Build our widget on start, but just reloads it later
        self.reload_widget()

    # Called when new character object is created.
    def create_default_data(self) -> dict:
        ''' Loads their existing data from file, or sets default data if no file exists '''

        print("Creating default data for character: " + self.title)

        # Data set upon first launch of program, or if file can't be loaded
        return {
            'title': self.title,
            'directory_path': self.directory_path,
            'visible': True,
            'tag': "character",
            'pin_location': "left", # New characters start pinned left

            'tab_color': "primary",  # Initial tab color matches color scheme
            'name_color': "primary",    # Flet color based on characters status of good, evil, neutral, or N/A
            'sex_color': "primary",    # Color of selected option in sex dropdown

            'Role': "Main",     # Char is either main, side, or bg. Doesn't show up in widget, but app can still change it  
            'Morality': "",
            'Sex': "",
            'Age': "",   # Text field
            
            'Physical Description': {
                'Race': "",
                'Skin Color': "",
                'Hair Color': "",   # Textfield
                'Eye Color': "",    # Textfield
                'Height': "",   # TextField
                'Weight': "",   # TextField
                'Build': "",    # 
                'Distinguishing Features': "",  # some sort of flet list
            },
            'Family':  {
                #'Love Interest': Character or str,
                'Love Interest': "",    # Sets a string
                'Father': "",   # Textfield with selectable options
                'Mother': "",    
                'Siblings': "",
                'Children': "",
                'Ancestors': "",
            },  
                
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
            'Dead': False,
            'Notes' : {},   # Category that says Notes on the left, then lists the expandable ft.TextField?
        }
        
        


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Body of the tab, which is the content of flet container
        body = ft.Container(
            expand=True,
            padding=6,
            #bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.ON_SECONDARY),
            content=ft.Column([
                ft.Text("hi from " + self.title),
                ft.Row(
                        wrap=True,
                       controls=[
                           #TODO addition of second dropdown for alignment
                            ft.Dropdown(        # Dropdown selection of good, evil, neutral, and n/a
                                label="Morality",
                                value=self.data['Morality'],
                                #padding=ft.padding.all(0),
                                color=self.data['name_color'],
                                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                options=[
                                    ft.DropdownOption(text="Undecided"),
                                    ft.DropdownOption(text="Good"),
                                    ft.DropdownOption(text="Neutral"),
                                    ft.DropdownOption(text="Evil"),
                                    ft.DropdownOption(text="None"),
                                    
                                ],
                                on_change=self.morality_change,
                            ),
                               
                            ft.Dropdown(      # Sex of each character
                                label="Sex",
                                value=self.data['Sex'],
                                #padding=ft.padding.all(0),
                                color=self.data['sex_color'],
                                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                options=[
                                    ft.DropdownOption(text="Male"),
                                    ft.DropdownOption(text="Female"),
                                    ft.DropdownOption(text="Other"),
                                    ft.DropdownOption(text="None"),
                                ],
                                on_change=self.sex_submit,
                            ),
                        ]
                    ),
                ]
            )

        )

        self.tab.content=body

        # Sets our header and the content of it
        content = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
                 
        )
          
        
        # Set our content
        self.content = content
        
    
    # Change our tab color of widget. Accepts a flet color as parameter
    def change_color(self, color):
        self.tab_color = color
        self.reload_widget()
        self.p.update()

    
    # Called when the morality dropdown is changed
    # Sets our new morality based on the choice selected. Applies changes to name_color, the rail, and the widget
    def morality_change(self, e):
        print("Morality change ran")
        self.data['Morality'] = e.control.value

        self.check_morality(e)
        self.reload_widget()    # Apply our changes to the name at top of widget

        self.p.update()
    
    # Called by the changes in characters morality. Changes the name_color property to reflect those changes
    def check_morality(self, e=None):
        # If we have the setting turned on to change char name colors, change them
        if app.settings.change_name_colors.value == True:
            print("color changing is true, we running the logic")
            # Check the morality and change color accordingly
            #TODO figure out color association & logic for assignment with morality alignments
            if self.data['Morality'] == "Good":
                self.name_color = ft.Colors.GREEN_200
            elif self.data['Morality'] == "Evil":
                self.name_color = ft.Colors.RED_200
            elif self.data['Morality'] == "Neutral":
                self.name_color = ft.Colors.GREY_300
            elif self.data['Morality'] == "Undecided":
                self.name_color = ft.Colors.GREY_300
            elif self.data['Morality'] == "None":    # Deselect all choices
                self.name_color = ft.Colors.PRIMARY
                self.data['Morality'] = None
                

        # If setting is turned off for char name colors, make all characters name_color the primary color scheme
        else:
            print("Color changing disabled, turning off all their colors")
            for character in app.active_story.characters:
                character.name_color = ft.Colors.PRIMARY
            # Apply our changes
            self.p.update()
            return

        # Reload the rail
        from ui.rails.characters_rail import reload_character_rail
        reload_character_rail(self.p)


    # Called when the textfield for writing in custom sex's is submitted
    # Adds our custom sex to our stories sex_options list
    def sex_submit(self, e):
        #print("sex submit ran")

        self.data['Sex'] = e.control.value

        if e.control.value == "None":
            self.data['Sex'] = None
        else:
            self.data['Sex'] = e.control.value

        print(self.data['Sex'])

        if self.data['Sex'] == "Male":
            self.sex_color = ft.Colors.BLUE
        elif self.data['Sex'] == "Female":
            self.sex_color = ft.Colors.PINK
        else:
            self.sex_color = ft.Colors.PRIMARY
        
        
        self.reload_widget()
        self.p.update()

    # Called when the age is changed. Changes the age data
    def age_change(self, e):
        #print("Age change ran")
        self.data['Age'].data = e.control.value
        print(self.data['Age'].data)

    # Called when the race is changed. Changes the race data
    def race_change(self, e):
        #print("Race change ran")
        self.data['Physical Description'].data['Race'] = e.control.value
        #print(self.data['Physical Description'].data['Race'])
        self.p.update()

    # Expand the tile to show physical descriptions
    def expand_physical_description(self, e):
        #print("expand physical description ran")
        pass
            



'''
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
        if app.settings.change_name_colors.value == True:
            print("color changing is true, we running the logic")
            # Check the morality and change color accordingly
            if self.data['Morality'].data == "Good":
                self.name_color = ft.Colors.GREEN_200
            elif self.data['Morality'].data == "Evil":
                self.name_color = ft.Colors.RED_200
            elif self.data['Morality'].data == "Neutral":
                self.name_color = ft.Colors.GREY_300
            elif self.data['Morality'].data == "N/A":
                self.name_color = ft.Colors.GREY_300
            elif self.data['Morality'].data == "Deselect":    # Deselect all choices
                self.name_color = ft.Colors.PRIMARY
                self.data['Morality'].value = None
                
            # Update our color
            self.data['Morality'].color = self.name_color

        # If setting is turned off for char name colors, make all characters name_color the primary color scheme
        else:
            print("Color changing disabled, turning off all their colors")
            for character in app.active_story.characters:
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
        if self.data['Sex'].data == "Deselect":
            self.data['Sex'].value = None
            self.reload_widget()    # When manually resetting value, must reload widget
        
        # If deselect is not clicked
        elif self.data['Sex'].data == "Male":
        # Checks that our data saved correctly, and changes color accordingly
            self.data['Sex'].color = ft.Colors.BLUE
            
        elif self.data['Sex'].data == "Female":
            self.data['Sex'].color = ft.Colors.PINK
        
        self.p.update()

    # Called when the age is changed. Changes the age data
    def age_change(self, e):
        print("Age change ran")
        self.data['Age'].data = e.control.value
        print(self.data['Age'].data)

    # Called when the race is changed. Changes the race data
    def race_change(self, e):
        print("Race change ran")
        self.data['Physical Description'].data['Race'] = e.control.value
        print(self.data['Physical Description'].data['Race'])
        self.p.update()

    # Expand the tile to show physical descriptions
    def expand_physical_description(self, e):
        print("expand physical description ran")
        

            
    "red"
    "pink",
    "purple",
    "blue",
    "cyan",
    "teal",
    "green",
    "lime",
    "yellow",
    "orange",
    "brown",
    "light grey",
    "grey",
    "none",
                                        
                          
    # Next row which shows the physical desciption. Expands when button clicked
    self.data['Physical Description'], 

    # Next row that shows family, which can expand right to left
    self.data['Family'],
                    
'''


