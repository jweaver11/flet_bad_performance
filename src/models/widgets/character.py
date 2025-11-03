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
            page = page,   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
            directory_path = directory_path,    # Directory where our json file is stored (characters/)
            story = story,   # Grabs our story reference so we can access story data and save our character in the right folder
            data = data,    # Passes in our data if we loaded it, or None if its a new character
        )

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            object=self,   # Pass in our own data so the function can see the actual data we loaded
            required_data={
                'tag': "character",
                'pin_location': "left" if data is None else data.get('pin_location', "left"),     # Start our characters on the left pin

                'tab_color': "primary",
                'name_color': "primary",
                'sex_color': "primary",
                'morality': str,
                'sex': str,
                'age': str,
                'physical_description': {
                    'Race': str,
                    'Skin Color': str,
                    'Hair Color': str,   
                    'Eye Color': str,    
                    'Height': str,   
                    'Weight': str,   
                    'Build': str,    
                    'Distinguishing Features': str,  
                },
                'family':  {
                    'Love Interest': str,    
                    'Father': str,   
                    'Mother': str,    
                    'Siblings': str,
                    'Children': str,
                    'Ancestors': str,
                },   
                'origin': {     
                    'birth_date': str,   
                    'hometown': str,     
                    'education': str,        
                },
                'trauma': str,
                'occupation': str,
                'goals': str,
                'personality': str,
                'backstory': str,
                'abilities': str,
                'is_dead': bool,    # Defaults to false
            },
        )
        
        #self.image = ""     # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False)    # Icon of character

        # Build our widget on start, but just reloads it later
        self.reload_widget()
    
    
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
        
        # Set our content
        self.body_container.content = body

        self._render_widget()
            


