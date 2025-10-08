'''
Most model classes really container 2 models: the character model itself and the associated widget model.
Inside of the 'data' dict, we store our characters model for the manipulative data...
the app will change. Everything else is built upon program launch so we can display it in the UI.
'''

import flet as ft
from models.widget import Widget
from models.story import Story
from handlers.verify_data import verify_data


# Sets our Character as an extended Widget object, which is a subclass of a flet Container
# Widget requires a title, tag, page reference, and a pin location
class Character(Widget):
    # Constructor
    def __init__(self, name: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):

        # Parent class constructor
        super().__init__(
            title = name,  # Name of character, but all objects have a 'title' for identification, so characters do too
            p = page,   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
            directory_path = directory_path,    # Directory where our json file is stored
            story = story,   # Grabs our story reference so we can access story data and save our character in the right folder
            data = data,    # Passes in our data if we loaded it, or None if its a new character
        )

        # Check if we loaded our settings data or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If our settings are new and not loaded, give it default data
        if not loaded:
            self.create_default_character_data()  # Create data defaults for our settings widgets

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            self.verify_character_data()
            
        
        #self.image = ""     # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False)    # Icon of character


        # Build our widget on start, but just reloads it later
        self.reload_widget()

    # Called when new character object is created.
    def create_default_character_data(self) -> dict:
        ''' Loads their existing data from file, or sets default data if no file exists '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}

        # Default data for new characters
        default_character_data = {
    
            'pin_location': "left",     # Overide default pin location of main
            'tag': "character",  

            'tab_color': "primary",  # Initial tab color matches color scheme
            'name_color': "primary",    # Flet color based on characters status of good, evil, neutral, or N/A
            'sex_color': "primary",    # Color of selected option in sex dropdown
 
            'morality': "",
            'sex': "",
            'age': "",   
            
            'physical_description': {
                'Race': "",
                'Skin Color': "",
                'Hair Color': "",   
                'Eye Color': "",    
                'Height': "",   
                'Weight': "",   
                'Build': "",    
                'Distinguishing Features': "",  # some sort of flet list
            },
            'family':  {
                'Love Interest': "",    # Name of another character, or str
                'Father': "",   # Textfield with selectable options
                'Mother': "",    
                'Siblings': "",
                'Children': "",
                'Ancestors': "",
            },  
            'trauma': "",
            'occupation': "",   
            'goals': "",    
            'origin': {     
                'birth_date': "",   
                'hometown': "",     
                'education': "",        
            },
            'personality': "",  
            'backstory': "",    
            'abilities': "",    
            'dead': False,
        }

        # Update existing data with any new default fields we added
        self.data.update(default_character_data)  
        self.save_dict()
        return
    
    # Verifies our loaded data to make sure it has all the fields we need, and adds any that are missing
    def verify_character_data(self):
        ''' Verify loaded any missing data fields in existing characters '''

        # Required data for all widgets and their types
        required_data_types = {
            'tag': str,
            'tab_color': str,
            'name_color': str,
            'sex_color': str,
            'morality': str,
            'sex': str,
            'age': str,
            'physical_description': dict,
            'family': dict,
            'trauma': str,
            'occupation': str,
            'goals': str,
            'origin': dict,
            'personality': str,
            'backstory': str,
            'abilities': str,
            'is_dead': bool,

        }

        # Defaults we can use for any missing fields
        data_defaults = {
            'tag': "character",  
            'tab_color': "primary",  # Initial tab color matches color scheme
            'name_color': "primary",    # Flet color based on characters status of good, evil, neutral, or N/A
            'sex_color': "primary",    # Color of selected option in sex dropdown
 
            'morality': "",
            'sex': "",
            'age': "",   
            
            'physical_description': {
                'Race': "",
                'Skin Color': "",
                'Hair Color': "",   
                'Eye Color': "",    
                'Height': "",   
                'Weight': "",   
                'Build': "",    
                'Distinguishing Features': "",  # some sort of flet list
            },
            'family':  {
                'Love Interest': "",    # Name of another character, or str
                'Father': "",   # Textfield with selectable options
                'Mother': "",    
                'Siblings': "",
                'Children': "",
                'Ancestors': "",
            },  
            'trauma': "",
            'occupation': "",   
            'goals': "",    
            'origin': {     
                'birth_date': "",   
                'hometown': "",     
                'education': "",        
            },
            'personality': "",  
            'backstory': "",    
            'abilities': "",    
            'is_dead': False,
        }

        # Run through our keys and make sure they all exist. If not, give them default values
        for key, required_data_type in required_data_types.items():
            if key not in self.data or not isinstance(self.data[key], required_data_type):
                self.data[key] = data_defaults[key]  

        self.data['tag'] = "character"   # Make sure our tag is always correct

        # Save our updated data
        self.save_dict()
        return
    
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

        pass

    # Called when the age is changed. Changes the age data
    def submit_age_change(self, e):
        #print("Age change ran")
        self.data['age'].data = e.control.value
        #print(self.data['Age'].data)
        self.save_dict()

    # Called when the race is changed. Changes the race data
    def submit_race_change(self, e):
        #print("Race change ran")
        pass
        

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
                                value=self.data['morality'],
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
                                value=self.data['sex'],
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
            


