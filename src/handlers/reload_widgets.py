from handlers.layout_widgets import layout_widgets

# Reload our widget list and how widget_row to hold our widgets
# Passes in a story object
def reload_widgets(story):
    story.visible_widgets.clear()    # clear our visible widget list
    for key, character in story.characters.items():
        if character.visible == True:        # This line is the error
            story.visible_widgets.append(character.widget)    # Make our list current with visible widgets


    layout_widgets(story.visible_widgets) # layout our widgets, and update everything
