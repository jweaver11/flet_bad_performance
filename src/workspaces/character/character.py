import flet as ft

# Class for each character. Requires passing in a name
class Character:
    def __init__(self, name):
        self.tag = "character"  # Tag for logic
        self.data = {
            'title': name,
            'age': "",
        }

        # How elements of our classes are stored in order to be rendered.
        # - Data variable itself
        # - An update method so controls can update the data directly
        # - Controls to render the data in the widget list
        self.age = ""
        def update_age(e):
            self.age = e.control.value
            print("Age updated to: ", self.age)
        self.age_controls = [
            ft.TextField(
                label="Age",
                hint_text="Age",
                value=self.age,
                width=200,
                multiline=True,
                on_change=update_age,
            ),
        ]

        self.family = {'Father': "", 'Mother': ""}
                       #'Siblings': [], 'Children': [], 'Spouse': [], 'Ancestors': []}
        def update_parents(e):
            self.parents[e.control.label] = e.control.value
            print("Parents updated to: ", self.parents)
        def create_parents_control():
            control = ft.TextField(
                    label="Father", # key
                    hint_text="Father", # key
                    value=self.age, # data
                    width=200,
                    multiline=True,
                    on_change=update_parents,
                ),
            return control 
        self.family_controls = [
            ft.Row([
                ft.Text("Family"),
                ft.TextField(
                    label="Father",
                    hint_text="Father",
                    value=self.age,
                    width=200,
                    multiline=True,
                    on_change=update_parents,
                ),
                ft.TextField(
                    label="Mother",
                    hint_text="Mother",
                    value=self.age,
                    width=200,
                    multiline=True,
                    on_change=update_parents,
                )
            ]),
        ]
        

        self.occupation = ""

        self.goals = ""

        self.physical_description = [
            # hair color, eye color, height, weight, etc.
        ]

        self.personality = ""

        self.backstory = ""

        self.abilities = {}

        self.notes = ""
        def update_notes(e):
            self.notes = e.control.value
            print("Notes updated to: ", self.notes)
        self.notes_controls = [
            ft.TextField(
                label="Notes",
                hint_text="Notes",
                value=self.notes,
                width=200,
                multiline=True,
                on_change=update_notes,
            ),
        ]

    
        def add_data(e):
            self.data["data_key"] = "data_value"
            print("Data added: ", self.data)


        self.visible = True     # Widget active and visible = True
        self.pin_location = "main"  # Start in main pin location
        self.widget = ft.Container()    # Set our widget as a flet container to hold the body
        # Body is a list of controls that use the object's data
        self.body = []  # flet list of controls to render rest of body
        # Update our widget so we can alter the char object class and re-render
        # Those updates into our widget, otherwise it would be static
        def update_widget():
            self.body.clear()  # Clear the body before updating

            for control in self.age_controls:
                self.body.append(control)

            for key, value in self.family.items():
                self.body.append(
                    ft.TextField(
                        label=key,
                        hint_text=key,
                        value=value,
                        width=200,
                        multiline=True,
                        on_change=update_parents,
                    )
                )
            
            for control in self.notes_controls:
                self.body.append(control)

            self.body.append(
                ft.TextButton(
                    on_click=add_data,
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


class Origin:
    birthplace: str
    birth_date: str
    hometown : str
    education : str

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
