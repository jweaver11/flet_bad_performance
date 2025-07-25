from models.user import user

story = user.active_story  # Get our story object from the user

def arrange_widgets():
    print("arrange widgets called")

    '''     Steal from other pins if main pin is empty
    if len(story.main_pin.controls) <= 0:
        if len(story.top_pin.controls) > 0:
            print("Steal from top pin")
        elif len(story.left_pin.controls) > 0:
            story.main_pin.controls.append(story.left_pin.controls[0])
            #...
    '''

    # Append a reference obj to the pin location based on its pin location tag
    def update_pin_location(obj):
        pin_location = obj.pin_location
        if pin_location == "top":
            story.top_pin.controls.append(obj)
        elif pin_location == "left":
            story.left_pin.controls.append(obj)
        elif pin_location == "main":
            story.main_pin.controls.append(obj)
        elif pin_location == "right":
            story.right_pin.controls.append(obj)
        elif pin_location == "bottom":
            story.bottom_pin.controls.append(obj)

    # Check our five pin locations.
    # If any object in them has a pin location different from its actual location, move them
    # Only check objects that have pin_location attribute (filter out spacing containers, dividers, etc.)
    for obj in story.top_pin.controls[:]:  # Use slice to avoid modifying list while iterating
        if hasattr(obj, 'pin_location') and obj.pin_location != "top":
            story.top_pin.controls.remove(obj)  # Remove from top pin if not in top pin location
            update_pin_location(obj)    # Add it to the correct pin location
    for obj in story.left_pin.controls[:]:
        if hasattr(obj, 'pin_location') and obj.pin_location != "left":
            story.left_pin.controls.remove(obj)
            update_pin_location(obj)
    for obj in story.main_pin.controls[:]:
        if hasattr(obj, 'pin_location') and obj.pin_location != "main":
            story.main_pin.controls.remove(obj)
            update_pin_location(obj)
    for obj in story.right_pin.controls[:]:
        if hasattr(obj, 'pin_location') and obj.pin_location != "right":
            story.right_pin.controls.remove(obj)
            update_pin_location(obj)
    for obj in story.bottom_pin.controls[:]:
        if hasattr(obj, 'pin_location') and obj.pin_location != "bottom":
            story.bottom_pin.controls.remove(obj)
            update_pin_location(obj)


