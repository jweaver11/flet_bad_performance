import flet as ft

# Class for each character. Requires passing in a name
class Character:
    def __init__(self, name):
        self.title = name  # Title of the character, used for identifier so all data objects have a title
        self.tag = "character"  # Tag for logic

        self.visible = True     # Widget active and visible = True
        self.pin_location = "main"  # Start in main pin location
        self.widget = ft.Container()    # Set our widget as a flet container to hold the body
        
        self.body = []  # flet list of controls to render rest of body

        # These 3 outside of data so they can render differently
        self.image = "" # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.age = ""
        self.sex = ""    # Add selecteble male, female, other - custom write in

        self.data = {
            'Family': {'Father': "", 'Mother': ""}, #'Siblings': [], 'Children': [], 'Spouse': [], 'Ancestors': []
            'Occupation': "",
            'Goals': "",
            'Origin': {
                'Birthplace': "",
                'Birth Date': "",
                'Hometown': "",
                'Education': "",
            },
            'Physical Description': {
                'Hair Color': "",
                'Eye Color': "",
                'Height': "",
                'Weight': "",
                'Build': "",
                'Distinguishing Features': "",
            },
            'Personality': "",
            'Backstory': "",
            'Abilities': "",
            'Notes' : "",
        }

        # Pass in our control and type of data
        def update_data(e, type):
            print(type)
            print("Type printed ^^^^^^^^^^^^^^^^^^^^^^^^^")
            self.data[e.control.key] = e.control.text
            print("Data updated: ", self.data)


        # Update our widget so we can alter the char object class and re-render
        # Those updates into our widget, otherwise it would be static
        def update_widget():
            self.body.clear()  # Clear the body before updating

            #self.body.append(ft.Image(src=self.image, width=100, height=100))
            self.body.append(ft.Container(ft.Icon(ft.Icons.PERSON, size=100), padding=10))

            # Render our built in data in a fixed formatted way, then format all other data
            # Differently afterwards

            # Run through all our data to render it
            for key, value in self.data.items():
                if not isinstance(value, dict):
                    self.body.append(
                        ft.Row(controls=[
                            ft.TextField(
                                label=key,
                                hint_text=key,
                                value=value,
                                width=200,
                                multiline=True,
                                on_change=lambda e: update_data(e, type(value)),
                            )
                        ])
                    )
                elif isinstance(value, dict):
                    row = ft.Row()
                    for sub_key, sub_value in value.items():
                        row.controls.append(
                            ft.TextField(
                                label=sub_key,
                                hint_text=sub_key,
                                value=sub_value,
                                width=200,
                                multiline=True,
                                on_change=lambda e: update_data(e, type(value)),
                            )
                        )
                    self.body.append(row)

            self.body.append(
                ft.TextButton(
                    on_click=lambda e: update_data(e, str),
                    text="Add Data",
                )
            )


        update_widget()  # Initialize the widget on startup


    # origin = Origin

    # unique data types, (not str)
    color : str
    icon : str

    tags : list[str]

    # Add ons that won't show by default
    race: str
    species : str
    parents = []
    # init comi


'''
tags = {
    main_character : bool
    side_character : bool
    background_character : bool
    good : bool
    evil : bool
    neutral : bool
    man : bool
    woman : bool
    alive : bool
}
'''
# Saving characters locally
# app_data_path = os.getenv("FLET_APP_STORAGE_TEMP")  # write to non-temp storage later /storage/data/characters
# my_file_path = os.path.join(app_data_path, "characters.json")
# with open(my_file_path, "w") as f:
    # f.write("My characters will go here")
