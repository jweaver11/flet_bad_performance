import os


# Set our data path for the app, and our path to our settings file
app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
settings_path = os.path.join(app_data_path, "settings")

# Set our path for all stories, and our active story
stories_directory_path = os.path.join(app_data_path, "stories")


# Create directories if they don't exist
os.makedirs(stories_directory_path, exist_ok=True)
os.makedirs(settings_path, exist_ok=True)



