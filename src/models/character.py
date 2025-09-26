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
        
    
    # Change our tab color of widget. Accepts a flet color as parameter
    def submit_color_change(self, color):
        colors = [
            "red",
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
        ]

        self.tab_color = color
        self.reload_widget()
        self.p.update()

    
    # Called when the morality dropdown is changed
    # Sets our new morality based on the choice selected. Applies changes to name_color, the rail, and the widget
    def submit_morality_change(self, e):
        print("Morality change ran")
        self.data['Morality'] = e.control.value

        morality = self.check_morality(e)
        if morality == "lawful_good":
            self.name_color = ft.Colors.GREEN_200
        #...

        self.reload_widget()    # Apply our changes to the name at top of widget
        # reload rail as well

        self.p.update()
    
    # Called by the changes in characters morality.
    def check_morality(self, e=None) -> str:
        # If we have the setting turned on to change char name colors, change them
        return "lawful_good"
     
        

        # USE MORALITY CHART (AND N/A), NOT JUST GOOD EVIL NEUTRAL
                

    # Called when the textfield for writing in custom sex's is submitted
    # Adds our custom sex to our stories sex_options list
    def submit_sex_change(self, e):
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
    def submit_age_change(self, e):
        #print("Age change ran")
        self.data['Age'].data = e.control.value
        print(self.data['Age'].data)

    # Called when the race is changed. Changes the race data
    def submit_race_change(self, e):
        #print("Race change ran")
        self.data['Physical Description'].data['Race'] = e.control.value
        #print(self.data['Physical Description'].data['Race'])
        self.p.update()
        

    # Expand the tile to show physical descriptions
    def expand_physical_description(self, e):
        #print("expand physical description ran")
        pass

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
                                on_change=self.submit_morality_change,
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
                                on_change=self.submit_sex_change,
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
            


