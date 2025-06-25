from handlers.layout_widgets import layout_widgets

def reload_widgets(story):

    # Adding our character widgets
    for character in story.characters:
        if character.visible:
            # If widget is not in visible_widgets, add it at the first None slot, else append
            if character.widget not in story.visible_widgets:
                try:
                    none_index = story.visible_widgets.index(None)
                    story.visible_widgets[none_index] = character.widget
                    print(f"{character.name} inserted at None slot {none_index}")
                except ValueError:
                    story.visible_widgets.append(character.widget)
                    print(f"{character.name} appended to visible_widgets")
        else:
            # If widget is in visible_widgets, replace with None
            if character.widget in story.visible_widgets:
                idx = story.visible_widgets.index(character.widget)
                story.visible_widgets[idx] = None
                print(f"{character.name} hidden, replaced with None at {idx}")

    
    


    layout_widgets(story.visible_widgets) # layout our widgets, and update everything

    print("reload widgets done")