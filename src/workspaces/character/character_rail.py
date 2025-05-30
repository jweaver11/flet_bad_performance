import flet as ft
from pagelets.characters import Character
from styles.styles import button_style

characters = []
characters.append(Character("Billy"))
characters.append(Character("Johnny"))
characters.append(Character("William"))

button_ref = ft.Ref[ft.TextButton]()
textfield_ref = ft.Ref[ft.TextField]()

# Control when 'Create Character' button is clicked
def add_character_click(e):
    button_ref.current.visible = False
    button_ref.current.update()
    textfield_ref.current.visible = True
    textfield_ref.current.focus()
    textfield_ref.current.update()

# Control submits in textfield when creating character
def on_textfield_submit(e):
    name = textfield_ref.current.value
    if name:
        characters.append({"name": name})
        print("Added character:", name)
    textfield_ref.current.value = ""
    textfield_ref.current.visible = False
    textfield_ref.current.update()
    button_ref.current.visible = True
    button_ref.current.update()

# When textbox is clicked off and nothing in it, reset to button
def on_textfield_deselect(e):
    name = textfield_ref.current.value
    if name == "":
        textfield_ref.current.visible = False
        button_ref.current.visible = True
        textfield_ref.current.update()
        button_ref.current.update()



# Rail for when the character workspace is selected
characters_rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    min_width=70,
    min_extended_width=300,
    group_alignment=-0.9,
    expand=True,
    #leading=Filter drop downs
    destinations=[
        ft.NavigationRailDestination(
            label="Filter Characters",  # Option to filter how all characters are show below (main, side, background, good, evil, neutral)
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS)
        ),  
        ft.NavigationRailDestination(
            label="Character 1", 
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS)
        ),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index)
)

# Function to add characters to char_rail. Returns a control. Call it through iteration of characters[]

# List of controls for the rail container
char_rail = [
    ft.TextButton("Character 1", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.TextButton("Character 2", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.TextButton("Character 3", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.TextButton("Create Character", icon=ft.Icons.WAVES_OUTLINED, style=button_style, ref=button_ref,
                  on_click=add_character_click),
    
    ft.TextField(
        ref=textfield_ref,
        visible=False,
        hint_text="Enter Character Name",
        width=200,
        on_submit=on_textfield_submit,
        on_tap_outside=on_textfield_deselect,
    ),
]
    
