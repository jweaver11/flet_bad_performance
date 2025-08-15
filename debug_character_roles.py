#!/usr/bin/env python3
"""
Debug script to check character Role data in pickle files
"""

import pickle
import os

def check_character_roles():
    characters_dir = "storage/data/stories/default_story/characters"
    
    if not os.path.exists(characters_dir):
        print(f"Characters directory does not exist: {characters_dir}")
        return
    
    pickle_files = [f for f in os.listdir(characters_dir) if f.endswith('.pkl')]
    
    if not pickle_files:
        print("No pickle files found")
        return
    
    print(f"Found {len(pickle_files)} character files:")
    print()
    
    for filename in pickle_files:
        file_path = os.path.join(characters_dir, filename)
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            
            print(f"📁 {filename}")
            print(f"   Title: {data.get('title', 'Unknown')}")
            print(f"   Pin Location: {data.get('pin_location', 'Unknown')}")
            
            char_data = data.get('character_data', {})
            role = char_data.get('Role', 'Unknown')
            print(f"   Role: {role}")
            
            print(f"   All character_data keys: {list(char_data.keys())}")
            print()
            
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            print()

if __name__ == "__main__":
    check_character_roles()
