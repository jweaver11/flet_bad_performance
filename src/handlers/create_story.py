from models.story import Story
import flet as ft

# Called when app creates a new story
def create_new_story(title: str, page: ft.Page) -> Story:
    ''' Creates the new story object, then saves it to a new folder WIP '''
    from constants.init import stories
    
    # Create a new story object and add it to our stories dict
    new_story = Story(title, page)
    stories[title] = new_story
    
    # page view - new story route and view

    return new_story
