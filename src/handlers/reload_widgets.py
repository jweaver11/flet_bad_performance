import flet as ft
from handlers.layout_widgets import layout_widgets

def reload_widgets(story):
    story.visible_widgets.clear()    # clear our visible widget list
    
    for key, character in story.characters.items():
        print(f"{key}: visible={character.visible}")
        if character.visible == True:        # This line is the error
            print(f"{key}: added to visible widgets")
            story.visible_widgets.append(character.widget)    # Make our list current with visible widgets


    layout_widgets(story.visible_widgets) # layout our widgets, and update everything

    print("reload widgets done")