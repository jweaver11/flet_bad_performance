import os


# Set our data path for the app
app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
# Set our settings path for the app
settings_path = os.path.join(app_data_path, "settings")

# Set our path for all stories, and our active story
stories_directory_path = os.path.join(app_data_path, "stories")


# Create directories if they don't exist
os.makedirs(stories_directory_path, exist_ok=True)
os.makedirs(settings_path, exist_ok=True)

# Active story path and all the workspaces inside of it
active_story_path = ""

# Sub paths dependent on the active_story path
content_path = ""
characters_path = ""
plot_and_timeline_path = ""
worldbuilding_path = ""
drawing_board_path = ""
notes_path = ""



# Called when we switch to another story
# Switches our file path to the new story
def set_active_story_path(story_title: str) -> str:
    global active_story_path, content_path, characters_path, plot_and_timeline_path, worldbuilding_path, drawing_board_path, notes_path

    # Updates our path to the active/open story 
    active_story_path = os.path.join(stories_directory_path, story_title)

    # Updates our paths for the workspaces
    content_path = os.path.join(active_story_path, "content")
    characters_path = os.path.join(active_story_path, "characters")
    plot_and_timeline_path = os.path.join(active_story_path, "plot_and_timeline")
    worldbuilding_path = os.path.join(active_story_path, "worldbuilding")
    drawing_board_path = os.path.join(active_story_path, "drawing_board")
    notes_path = os.path.join(active_story_path, "notes")
    
    
    return active_story_path



