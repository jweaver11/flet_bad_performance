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
                'alignment1': str, #lawful, neutral, chaotic, none
                'alignment2': str, #good, neutral, evil, none
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
                'strengths': {
                    'physical': str,
                    'mental': str,
                    'social': str,
                },
                'weaknesses': {
                    'physical': str,
                    'mental': str,
                    'social': str,
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
        
        self.icon = ft.Icon(ft.Icons.PERSON, size=100, expand=False)    # Icon of character

        # Build our widget on start, but just reloads it later
        self.reload_widget()
    

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Rebuild out tab to reflect any changes
        self.reload_tab()

        if self.data['is_active_tab']:
            self.icon = ft.Icon(ft.Icons.PERSON, size=100, color="primary", expand=False)
        else:
            self.icon = ft.Icon(ft.Icons.PERSON_OUTLINE, size=100, color="disabled", expand=False)

        # Body of the tab, which is the content of flet container
        body = ft.Container(
            expand=True,                # Takes up maximum space allowed in its parent container
            padding=6,                  # Padding around everything inside the container
            content=ft.Column([                 # The column that will hold all our stuff top down
                self.icon,                          # The icon above the name
                ft.Text("hi from " + self.title),           # Text that shows the title
                ft.Row(                     # The row that will hold our dropdowns
                        wrap=True,          # Allows moving into columns/multiple lines if dropdowns don't fit
                        controls=[          # All flet controls inside our Row
                           #TODO addition of second dropdown for alignment
                            ft.Dropdown(        # Dropdown selection of lawful, chaotic, neutral, and n/a
                                label="alignment1",           # Label at top of dropdown 
                                value=self.data['alignment1'],        # Value selected in the drop down
                                #padding=ft.padding.all(0),
                                color=self.data['name_color'],      # Color of the dropdown text
                                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),         # Style of the text in the dropdown
                                options=[           # Options for the dropdown
                                    ft.DropdownOption(text="Undecided"),
                                    ft.DropdownOption(text="Lawful"),
                                    ft.DropdownOption(text="Neutral"),
                                    ft.DropdownOption(text="Chaotic"),
                                    ft.DropdownOption(text="None"),
                                    
                                ],
                                #n_change=self.submit_alignment1_change,
                            ),
                            ft.Dropdown(        # Dropdown selection of good, evil, neutral, and n/a
                                label="alignment2",           # Label at top of dropdown 
                                value=self.data['alignment2'],        # Value selected in the drop down
                                #padding=ft.padding.all(0),
                                color=self.data['name_color'],      # Color of the dropdown text
                                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),         # Style of the text in the dropdown
                                options=[           # Options for the dropdown
                                    ft.DropdownOption(text="Undecided"),
                                    ft.DropdownOption(text="Good"),
                                    ft.DropdownOption(text="Neutral"),
                                    ft.DropdownOption(text="Evil"),
                                    ft.DropdownOption(text="None"),
                                    
                                ],
                                #n_change=self.submit_alignment1_change,
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
                                #TODO on "other" selection, open a text field to specify
                                #on_change=self.submit_sex_change,
                            ),
            
                            ft.TextField(   # Text field for race input
                                label ="Race"
                            ),
                            #gotta make it so it doesn't make a super long field if dragged
                            ft.TextField(  # Text field for age input
                                label ="Age"
                            ),
                            #same as above but also both need to update data on change
                        ]
                    ),
                ]
            )

        )     
        
        # Set our content to the body_container (from Widget class) as the body we just built
        self.body_container.content = body

        # Call render widget (from Widget class) to update the UI
        self._render_widget()
            


