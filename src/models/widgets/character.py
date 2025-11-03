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
            title = name,  
            page = page,   
            directory_path = directory_path, 
            story = story,   
            data = data,    
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
                'data1': str,
                'data2': "coding sux",
            },
        )
        
        #self.image = ""     # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False)    # Icon of character

        # Build our widget on start, but just reloads it later
        self.reload_tab()
        self.reload_widget()
    

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
                                #n_change=self.submit_morality_change,
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
                                #on_change=self.submit_sex_change,
                            ),
                        ]
                    ),
                ]
            )

        )     
        
        # Set our content
        self.body_container.content = body

        self._render_widget()
            


