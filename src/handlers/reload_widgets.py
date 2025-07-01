from handlers.layout_widgets import layout_widgets
from models.story import story

def reload_widgets():
    
    visible_widgets = []
    # Grab our widgets dict from story object
    for widget in story.widgets.values():
        # If they are visible, add the control (rendered widget) to our list
        if widget.visible == True:
            visible_widgets.append(widget.control)
        
    # layout our list
    layout_widgets(visible_widgets) # layout our widgets, and update everything

    print("reload widgets done")