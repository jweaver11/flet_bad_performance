from handlers.layout_widgets import layout_widgets

def reload_widgets(story):

    for character in story.characters:
        if character.visible and character.widget not in story.visible_widgets:
            print(f"{character.name} added to visible widgets")
            story.visible_widgets.append(character.widget)
        elif character.widget in story.visible_widgets and not character.visible:
            print(f"{character.name} removed from visible widgets")
            story.visible_widgets.remove(character.widget)
    
    


    layout_widgets(story.visible_widgets) # layout our widgets, and update everything

    print("reload widgets done")