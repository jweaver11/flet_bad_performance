from handlers.layout_widgets import layout_widgets

# Reload our widget list and how widget_row to hold our widgets
# Passes in a story object
def reload_widgets(story):
    story.active_widgets.clear()
    for char_name in story.characters:
        character = story.characters[char_name]
        if character.visible == True:        # This line is the error
            story.active_widgets.append(character.widget)    # Make our list current with visible widgets

    layout_widgets(story.active_widgets) # layout our widgets, and update everything
