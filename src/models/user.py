'''
Our user of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model meaning...
All other files can import this function without issues
'''

from models.story import Story
import os
import flet as ft


class User:
    # Constructor
    def __init__(self):

        # Declares settings and workspace rail here, but we create/load them later in main
        self.settings = None
        self.all_workspaces_rail = None   # All workspaces rail
        
        # Dict of all our stories.
        self.stories = {}

        
        # Load existing stories from the directory
        self.load_stories()
        
        # If no stories were loaded, create a default story
        if not self.stories:
            print("No existing stories found, creating default story")
            self.create_new_story("default_story")
        
        # When settings is created, it uses default story if none exists
        self.active_story = self.stories['default_story']

        
        
    # Called on program launch 
    def load_stories(self):
        ''' Loads all stories from the stories directory into our user object '''

        from constants import data_paths

        #print("Loading stories from directory...")
        
        # Check if stories directory exists
        if not os.path.exists(data_paths.stories_directory_path):
            print("Stories directory does not exist, creating it.")
            os.makedirs(data_paths.stories_directory_path)
            return

        # Iterate through all files in the stories directory
        for filename in os.listdir(data_paths.stories_directory_path):
            # For filetypes that end in .json inside of stories_directory_path
            if filename.endswith(".json"):
                # Create a new story object inside our self.stories with the title of the file (minus .json)
                story_title = filename.replace(".json", "")
                
                try:
                    # Create story object - this will load its data automatically
                    story = Story(story_title)
                    self.stories[story_title] = story
                    #print(f"Loaded story: {story_title}")
                    
                except Exception as e:
                    print(f"Error loading story {story_title}: {e}")
                    
        #print(f"Loaded {len(self.stories)} stories total")


    # Called when opening a different story, or when new story is created
    def set_new_active_story(self) -> Story:
        ''' Sets a new active story based on the title given WIP '''

        # When settings is created, it uses default story if none exists
        self.active_story = self.stories[self.settings.data['active_story']]


    # Called when user creates a new story
    def create_new_story(self, title: str) -> Story:
        ''' Creates the new story object, then saves it to a new folder WIP '''
        
        # Create a new story object and add it to our stories dict
        new_story = Story(title)
        self.stories[title] = new_story
        self.active_story = new_story
        # Save story dict (doesnt exist yet)

        self.set_new_active_story(title)

        return new_story
    


# Sets our global user object
user = User()