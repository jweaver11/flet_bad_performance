from models.user import user

story = user.stories['empty_story']  # Get our story object from the user

def arrange_widgets():
    print("arrange widgets called")

    for char in story.characters:   # Run through our objects in story
        # Add them to their pin location list if not already there
        if char.pin_location == "top" and char not in story.top_pin_obj:   
            story.top_pin_obj.append(char)
            # Remove them from other pin locations if they exist there
            if char in story.left_pin_obj:
                story.left_pin_obj.remove(char)
            elif char in story.main_pin_obj:
                story.main_pin_obj.remove(char)
            elif char in story.right_pin_obj:
                story.right_pin_obj.remove(char)
            elif char in story.bottom_pin_obj:
                story.bottom_pin_obj.remove(char)

        elif char.pin_location == "left" and char not in story.left_pin_obj:
            story.left_pin_obj.append(char)
            if char in story.top_pin_obj:
                story.top_pin_obj.remove(char)
            elif char in story.main_pin_obj:
                story.main_pin_obj.remove(char)
            elif char in story.right_pin_obj:
                story.right_pin_obj.remove(char)
            elif char in story.bottom_pin_obj:
                story.bottom_pin_obj.remove(char)

        elif char.pin_location == "main" and char not in story.main_pin_obj:
            story.main_pin_obj.append(char)
            if char in story.top_pin_obj:
                story.top_pin_obj.remove(char)
            elif char in story.left_pin_obj:
                story.left_pin_obj.remove(char)
            elif char in story.right_pin_obj:
                story.right_pin_obj.remove(char)
            elif char in story.bottom_pin_obj:
                story.bottom_pin_obj.remove(char)

        elif char.pin_location == "right" and char not in story.right_pin_obj:
            story.right_pin_obj.append(char)
            if char in story.top_pin_obj:
                story.top_pin_obj.remove(char)
            elif char in story.left_pin_obj:
                story.left_pin_obj.remove(char)
            elif char in story.main_pin_obj:
                story.main_pin_obj.remove(char)
            elif char in story.bottom_pin_obj:
                story.bottom_pin_obj.remove(char)

        elif char.pin_location == "bottom" and char not in story.bottom_pin_obj:
            story.bottom_pin_obj.append(char)
            if char in story.top_pin_obj:
                story.top_pin_obj.remove(char)
            elif char in story.left_pin_obj:
                story.left_pin_obj.remove(char)
            elif char in story.main_pin_obj:
                story.main_pin_obj.remove(char)
            elif char in story.right_pin_obj:
                story.right_pin_obj.remove(char)

