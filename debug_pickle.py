#!/usr/bin/env python3
"""
Debug script to test pickle file integrity
Run this from the project root to check if pickle files are valid
"""

import pickle
import os

def test_pickle_file(filepath):
    """Test if a pickle file can be loaded"""
    try:
        with open(filepath, 'rb') as f:
            obj = pickle.load(f)
        print(f"✓ Successfully loaded {filepath}")
        print(f"  Object type: {type(obj)}")
        if hasattr(obj, 'title'):
            print(f"  Title: {obj.title}")
        if hasattr(obj, 'tag'):
            print(f"  Tag: {obj.tag}")
        if hasattr(obj, 'character_data'):
            print(f"  Character data keys: {list(obj.character_data.keys())}")
        print()
        return True
    except Exception as e:
        print(f"✗ Failed to load {filepath}: {e}")
        return False

def main():
    characters_dir = "storage/data/stories/default_story/characters"
    
    if not os.path.exists(characters_dir):
        print(f"Characters directory does not exist: {characters_dir}")
        return
    
    pickle_files = [f for f in os.listdir(characters_dir) if f.endswith('.pkl')]
    
    if not pickle_files:
        print("No pickle files found in characters directory")
        return
    
    print(f"Found {len(pickle_files)} pickle files:")
    for filename in pickle_files:
        file_path = os.path.join(characters_dir, filename)
        file_size = os.path.getsize(file_path)
        print(f"  {filename} ({file_size} bytes)")
    
    print("\nTesting pickle files:")
    success_count = 0
    for filename in pickle_files:
        file_path = os.path.join(characters_dir, filename)
        if test_pickle_file(file_path):
            success_count += 1
    
    print(f"Successfully loaded {success_count}/{len(pickle_files)} pickle files")

if __name__ == "__main__":
    main()
