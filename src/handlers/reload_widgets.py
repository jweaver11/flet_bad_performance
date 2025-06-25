from handlers.layout_widgets import layout_widgets

def reload_widgets(story):
    story.visible_widgets.clear()    # clear our visible widget list
    
    for character in story.characters:
        print(f"{character.name}")
        if character.visible == True:        # This line is the error
            print(f"{character.name} added to visible widgets")
            story.visible_widgets.append(character.widget)    # Make our list current with visible widgets


    layout_widgets(story.visible_widgets) # layout our widgets, and update everything

    print("reload widgets done")