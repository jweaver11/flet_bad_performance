''' 
Master Story class that contains data and methods for the entire story 
This is a dead-end model. Imports nothing else from project, or things will ciruclar import
'''

import flet as ft
import json
import os
import pickle       # Saving python objects to files since json won't work

class Story:
    # Constructor for when new story is created
    def __init__(self, title: str, path: str):
       
        self.title=title # Gives our story a title when its created
        self.path=path  # Gives us a path to save/load the story

        self.top_pin = ft.Row(height=0, spacing=0, controls=[])
        self.left_pin = ft.Column(width=0, spacing=0, controls=[])
        self.main_pin = ft.Row(expand=True, spacing=0, controls=[])
        self.right_pin = ft.Column(width=0, spacing=0, controls=[])
        self.bottom_pin = ft.Row(height=0, spacing=0, controls=[])

        # Our master row that holds all our widgets
        self.widgets = ft.Row(spacing=0, expand=True, controls=[])


        # Master stack that holds our widgets
        # And our drag targets when we start dragging widgets.
        # We do this so there is a receiver (drag target) for the widget even if a pin is empty and hidden
        self.master_stack = ft.Stack(expand=True, controls=[self.widgets])


        # Default active workspace rail if none selected/on startup rn
        self.default_rail = [ft.TextButton("Select a workspace")]

        # Map of all the workspace rails - Rails must be a list of flet controls
        self.workspace_rails = {
            0: self.default_rail,
        }  

        # Format our active rail 
        self.active_rail = ft.Column(  
            spacing=0,
            controls=self.workspace_rails[0],    # On startup, set to char rail
        )  

        # Make a list for positional indexing
        self.characters = []    # Dict of character object. Used for storing/deleting characters
        
        # Store page reference for loading objects later
        self.page_reference = None

    # Initialize story with saved data - call this after page is available
    def initialize_with_saved_data(self, page_reference):
        """Load all saved objects when the story is initialized with a page reference"""
        self.page_reference = page_reference
        self.load_all_characters(page_reference)
        print(f"Story '{self.title}' initialized with {len(self.characters)} saved characters")
            

    # Add our created object to story. This will add it to any lists it should be in, pin location, etc.
    # All our story objects are extended flet containers, and require a title, pin location, tag,...
    def add_object_to_story(self, obj):
        print("Adding object in story: " + obj.title)

        # Runs to save our character to our story object, and save it to file
        def save_character(obj):
            print("save character called")
            self.characters.append(obj)
            self.save_object_to_file(obj)

        # Is called when the parent f
        def save_chapter(obj):
            print("save chapter called")
            print(obj)


        # Checks our objects tag, then figures out what to do with it
        if hasattr(obj, 'tag'):
            # Characters
            if obj.tag == "character":
                save_character(obj)
            # Chapters
            elif obj.tag == "chapter":
                save_chapter(obj)
            
            else:
                print("object does not have a valid tag")

            # Checks our pin location and then adds it to a pin
            if hasattr(obj, 'pin_location'):  
                self.add_object_to_pin(obj)

            # If object has no pin location, we don't pin it anywhere
            else:
                print("Object does not have a pin location, did not pin to story")

        # If no tag exists, we do nothing
        else:
            print("obj has no tag, did not save it")


    # Adds our object to one of our five pin locations
    def add_object_to_pin(self, obj):
        print("add object to pin called")

        # check objects pin and that its not already in that pin
        if obj.pin_location == "top" and obj not in self.top_pin.controls:
            self.top_pin.controls.append(obj)
        elif obj.pin_location == "left" and obj not in self.left_pin.controls:
            self.left_pin.controls.append(obj)
        elif obj.pin_location == "main" and obj not in self.main_pin.controls:
            self.main_pin.controls.append(obj)  
        elif obj.pin_location == "right" and obj not in self.right_pin.controls:
            self.right_pin.controls.append(obj)
        elif obj.pin_location == "bottom" and obj not in self.bottom_pin.controls:
            self.bottom_pin.controls.append(obj)
        else:
            print("object has an invalid pin location")

    # Handles saving our object to a file for permanent data storage, not just client
    def save_object_to_file(self, obj):
        print("object saved to file called")

        if obj.tag == "character":
            characters_dir = self.path + "/characters/"
            # Ensure the characters directory exists
            os.makedirs(characters_dir, exist_ok=True)
            
            # Create a safe filename from the character's title
            safe_filename = "".join(c for c in obj.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_filename = safe_filename.replace(' ', '_')
            character_file_path = os.path.join(characters_dir, f"{safe_filename}.pkl")
            
            print(f"Attempting to save character to: {character_file_path}")
            print(f"Character object type: {type(obj)}")
            print(f"Character has title: {hasattr(obj, 'title')}")
            print(f"Character has character_data: {hasattr(obj, 'character_data')}")
            
            try:
                # Try to save with a safer approach - create a copy without problematic references
                safe_obj = self.create_serializable_character_copy(obj)
                
                with open(character_file_path, 'wb') as f:
                    pickle.dump(safe_obj, f)
                    
                # Verify the file was written
                file_size = os.path.getsize(character_file_path)
                print(f"Character '{obj.title}' saved to {character_file_path} (size: {file_size} bytes)")
                
                if file_size == 0:
                    print("WARNING: Saved file is 0 bytes!")
                    
            except Exception as e:
                print(f"Error saving character to file: {e}")
                import traceback
                traceback.print_exc()
            print("Saving character to file completed")

    def create_serializable_character_copy(self, character):
        """Create a copy of character that can be safely pickled"""
        try:
            # First try to pickle the original object to see if it works
            import io
            buffer = io.BytesIO()
            pickle.dump(character, buffer)
            buffer.seek(0)
            # If we got here, the original object is serializable
            return character
        except Exception as e:
            print(f"Original character not serializable: {e}")
            # Create a minimal serializable version
            serializable_data = {
                'title': character.title,
                'tag': character.tag,
                'pin_location': getattr(character, 'pin_location', None),
                'character_data': {},
                'class_name': character.__class__.__name__
            }
            
            # Extract values from character_data
            if hasattr(character, 'character_data'):
                for key, value in character.character_data.items():
                    try:
                        if hasattr(value, 'value'):
                            serializable_data['character_data'][key] = value.value
                        elif hasattr(value, 'data'):
                            serializable_data['character_data'][key] = value.data
                        else:
                            serializable_data['character_data'][key] = str(value)
                    except Exception as ve:
                        print(f"Could not serialize character_data[{key}]: {ve}")
                        serializable_data['character_data'][key] = None
            
            return serializable_data

    # Load an object from file
    def load_object_from_file(self, file_path, page_reference):
        """Load a saved object from file"""
        try:
            with open(file_path, 'rb') as f:
                obj = pickle.load(f)
            
            # Check if it's a full character object or serializable data
            if isinstance(obj, dict) and 'class_name' in obj:
                # It's serialized data, need to reconstruct the character
                obj = self.reconstruct_character_from_data(obj, page_reference)
            else:
                # It's a full object, just update page references
                if hasattr(obj, 'p'):
                    obj.p = page_reference
                    
                # Update any controls that might need page reference
                if hasattr(obj, 'character_data'):
                    for key, control in obj.character_data.items():
                        if hasattr(control, 'page'):
                            control.page = page_reference
                        
            print(f"Successfully loaded object '{obj.title if hasattr(obj, 'title') else 'Unknown'}' from {file_path}")
            return obj
        except Exception as e:
            print(f"Error loading object from file {file_path}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def reconstruct_character_from_data(self, data, page_reference):
        """Reconstruct a character object from serialized data"""
        try:
            # Import Character class dynamically to avoid circular imports
            from models.character import Character
            
            # Create a new character with the saved title
            character = Character(data['title'], page_reference)
            
            # Restore basic properties
            if 'pin_location' in data:
                character.pin_location = data['pin_location']
                
            # Restore character data values
            if 'character_data' in data:
                for key, value in data['character_data'].items():
                    if key in character.character_data:
                        if hasattr(character.character_data[key], 'value'):
                            character.character_data[key].value = value
                        elif hasattr(character.character_data[key], 'data'):
                            character.character_data[key].data = value
            
            print(f"Successfully reconstructed character '{character.title}' from serialized data")
            return character
        except Exception as e:
            print(f"Error reconstructing character from data: {e}")
            return None

    # Load all characters from the characters directory
    def load_all_characters(self, page_reference):
        """Load all saved characters"""
        characters_dir = self.path + "/characters/"
        if not os.path.exists(characters_dir):
            print("Characters directory does not exist")
            return
            
        pkl_files = [f for f in os.listdir(characters_dir) if f.endswith('.pkl')]
        print(f"Found {len(pkl_files)} character files to load: {pkl_files}")
        
        for filename in pkl_files:
            file_path = os.path.join(characters_dir, filename)
            character = self.load_object_from_file(file_path, page_reference)
            if character:
                # Add to characters list if not already present
                if character not in self.characters:
                    self.characters.append(character)
                    
                # Add to appropriate pin location if not already present
                if hasattr(character, 'pin_location'):
                    self.add_object_to_pin(character)
                    
        print(f"Loaded {len(self.characters)} characters total")



    # Delete an object from the story. Only works for certain objects
    def delete_object_from_story(self, obj):
        print("Removing object from story: " + obj.title)

        

        # Remove from characters list if it is a character
        if hasattr(obj, 'tag') and obj.tag == "character":
            # Chck our characters pin location, and remove its reference from there
            if hasattr(obj, 'pin_location'):
                if obj.pin_location == "top":
                    self.top_pin.controls.remove(obj)
                elif obj.pin_location == "left":
                    self.left_pin.controls.remove(obj)
                elif obj.pin_location == "main":
                    self.main_pin.controls.remove(obj)
                elif obj.pin_location == "right":
                    self.right_pin.controls.remove(obj)
                elif obj.pin_location == "bottom":
                    self.bottom_pin.controls.remove(obj)
            # Remove object from the characters list
            if obj in self.characters:
                self.characters.remove(obj)
            

        # delete_from_file()




# Add all this to user file??
# Save stories locally - folder structure:
# user/stories/story_name/
# - characters/character
# - workspace_name/...