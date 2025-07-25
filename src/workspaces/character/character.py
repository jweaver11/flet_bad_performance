import flet as ft
from models.user import user
from handlers.render_widgets import render_widgets, master_widget_row, pin_drag_targets, stack

story = user.active_story  # Get our story object from the user
# Class for each character. Requires passing in a name
class Character(ft.Container):
    def __init__(self, name, page: ft.Page):
        self.title = name  # Title of the character, used for identifier so all data objects have a title
        self.tag = "character"  # Tag for logic

        self.pin_location = "left"  # Start in main pin location
        story.left_pin.controls.append(self)  # Add to left pin location
        
        self.controls = []  # flet list of controls to render rest of body

        self.tags = {
            'main_character': True,      
            'side_character' : True,     
            'background_character': True,     
            #good : bool
            #evil : bool
            #neutral : bool
            #man : bool
            #woman : bool
            #alive : bool
        }

        # These 3 outside of data so they can render differently
        self.image = "" # Use AI to gen based off characteristics, or mini icon generator, or upload img
        self.age = ""
        self.sex = ""    # Add selecteble male, female, other - custom write in

        self.char_data = {
            'Good': True,
            'Evil': False,
            'Neutral': False,
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
            print("Data updated: ", self.char_data)


        # Update our widget so we can alter the char object class and re-render
        # Those updates into our widget, otherwise it would be static
        def update_widget():
            self.controls.clear()  # Clear the body before updating

            #self.body.append(ft.Image(src=self.image, width=100, height=100))
            self.controls.append(ft.Container(ft.Icon(ft.Icons.PERSON, size=100), padding=10))

            # Render our built in data in a fixed formatted way, then format all other data
            # Differently afterwards

            # Run through all our data to render it
            for key, value in self.char_data.items():
                if not isinstance(value, dict):
                    self.controls.append(
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
                    self.controls.append(row)

            self.controls.append(
                ft.TextButton(
                    on_click=lambda e: update_data(e, str),
                    text="Add Data",
                )
            )


        update_widget()  # Initialize the widget on startup

        def on_drag_start(e):
            print("\ndrag start called\n")

            stack.controls.extend(pin_drag_targets)  # Add the drag target pins to the stack
            stack.update()

        def on_drag_complete(e):    # Has no cancellation method, meaning errors if not dropped in workspace
            print("Drag complete called")
            stack.controls.clear()
            stack.controls.append(master_widget_row)  # Re-add the widget row to the stack
            stack.update()

        def hide(e):
            self.visible = False
            render_widgets(page)
            page.update()

        # Make a markdown as content of container
        super().__init__(
            expand=True,
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor=ft.Colors.GREY_900,
            content=ft.Column(spacing=0, controls=[
                ft.Stack([
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Draggable(
                                group="widgets",
                                content=ft.TextButton(self.title),
                                data=self,       # Pass our object as the data so we can access it
                                on_drag_start=on_drag_start,
                                on_drag_complete=on_drag_complete,
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(
                                on_click=hide,
                                icon=ft.Icons.CLOSE_ROUNDED
                    )])
                ]),
                ft.Divider(color=ft.Colors.PRIMARY),
                ft.Container(       # Body of the widget
                    expand=True,
                    content=ft.Column(self.controls)
                )
            ])
        )

    # origin = Origin

    # unique data types, (not str)
    color : str
    icon : str

    # Add ons that won't show by default
    race: str
    species : str
    parents = []



# Make widget container contain markdown for rendering, and scrollable

