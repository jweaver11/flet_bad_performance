

def check_story_unique(story_title: str) -> bool:
    ''' Checks if the given story title is unique among existing stories '''
    from models.app import app

    
    for story in app.stories.values():
        if story.title == story_title:
            return False
    return True