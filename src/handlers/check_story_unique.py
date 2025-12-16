import flet as ft

def story_is_unique(new_story_title: str, text_field: ft.TextField) -> bool:
    ''' Checks if the given story title is unique among existing stories '''
    from models.app import app
    
    # Compare against all existing story titles so we don't have any duplicates
    for story in app.stories.values():
        if story.title.lower() == new_story_title.lower():
            text_field.error_text = "Title must be unique"  # Set error text on the text field
            return False
        
    # Reset error text if unique
    text_field.error_text = None
    return True