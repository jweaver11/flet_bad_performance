from models.user import user

story = user.active_story  # Get our story object from the user

def arrange_widgets():
    print("arrange widgets called")
    

    # Append a reference obj (pointer) to the pin location based on its pin location tag
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
    for obj in story.top_pin.controls[:]:  # Check our first of five pin locations
    # Use slice to avoid modifying list while iterating
        if hasattr(obj, 'pin_location') and obj.pin_location != "top":  # Check if pin_location does not match its actual location
            story.top_pin.controls.remove(obj)  # Remove from top pin if not matching
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



    # Steal from other pins if main pin is empty. Makes UI look prettier
    if len(story.main_pin.controls) == 0:   # Check if main pin is empty
        
        if len(story.top_pin.controls) > 0: # If it is, check all other pins to steal from
            for obj in story.top_pin.controls[:]:  # Run through our objects to find the first visible one
                if obj.visible == True:
                    story.top_pin.controls.remove(obj)  # Remove from top pin
                    story.main_pin.controls.append(obj)  # Add to main pin
                    obj.pin_location = "main"  # Update pin location
                    print("Stole from top pin")
                    break   # Exit our for loop
        elif len(story.left_pin.controls) > 0:  # If top is empty, check left
            for obj in story.left_pin.controls[:]:
                if obj.visible == True:
                    story.left_pin.controls.remove(obj)
                    story.main_pin.controls.append(obj)
                    obj.pin_location = "main"
                    print("Stole from left pin")
                    break
        elif len(story.right_pin.controls) > 0:  # If top and left are empty, check right
            for obj in story.right_pin.controls[:]:
                if obj.visible == True:
                    story.right_pin.controls.remove(obj)
                    story.main_pin.controls.append(obj)
                    obj.pin_location = "main"
                    print("Stole from right pin")
                    break
        elif len(story.bottom_pin.controls) > 0:  # If top, left, and right are empty, check bottom
            for obj in story.bottom_pin.controls[:]:
                if obj.visible == True:
                    story.bottom_pin.controls.remove(obj)
                    story.main_pin.controls.append(obj)
                    obj.pin_location = "main"
                    print("Stole from bottom pin")
                    break
        else:
            print("No visible widgets, so we did not steal from other pins")


