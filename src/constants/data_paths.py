import os


# Set our data path for the app
app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
# Set our settings path for the app
settings_path = os.path.join(app_data_path, "settings")

# Set our path for all stories, and our active story
stories_path = os.path.join(app_data_path, "stories")

# Create directories if they don't exist
os.makedirs(stories_path, exist_ok=True)
os.makedirs(settings_path, exist_ok=True)

#active_story_path: str | None
active_story_path = ""

# Called when we switch to another story
# Switches our file path to the new story
def set_active_story_path(story_title: str) -> str:
    global active_story_path

    print("Old active story path: ", active_story_path)
    
    active_story_path = os.path.join(stories_path, story_title)
    print("new active story path: ", active_story_path)
    
    return active_story_path



