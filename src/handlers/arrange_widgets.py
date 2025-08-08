from models.user import user

story = user.active_story  # Get our story object from the user

# Called by other functions after a completed drag. This check the widgets in each pins 'pin_location' tag...
# And if they don't match their actual pin location, it moves them to the correct one BASED of the tag
# Also handles making sure there is always a widget in the main_pin, so long as there is at least 1 visible widget
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
            story.main_pin.tabs.append(obj)
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
    for obj in story.main_pin.tabs[:]:
        if hasattr(obj, 'pin_location') and obj.pin_location != "main":
            story.main_pin.tabs.remove(obj)
            update_pin_location(obj)
    for obj in story.right_pin.controls[:]:
        if hasattr(obj, 'pin_location') and obj.pin_location != "right":
            story.right_pin.controls.remove(obj)
            update_pin_location(obj)
    for obj in story.bottom_pin.controls[:]:
        if hasattr(obj, 'pin_location') and obj.pin_location != "bottom":
            story.bottom_pin.controls.remove(obj)
            update_pin_location(obj)

    # Called when main pin is empty or has no visible widgets
    # Function to steal from our other pins so UI looks prettier and consistent
    def steal_from_other_pins():
        print("steal from other pins called")

        # If pin is NOT empty. Pin's can hold widgets that are not visible, so we check that as well
        if len(story.top_pin.controls) > 0: 
            for obj in story.top_pin.controls[:]:  
                if obj.visible == True:     # If there is at least one visible widget
                    obj.pin_location = "main"  # Update pin location
                    story.main_pin.controls.append(obj)  # Add object to main pin
                    #story.main_pin.update()
                    story.top_pin.controls.remove(obj)  # Remove it from top pin
                    #story.top_pin.update()
                    print("Stole from top pin")
                    break   # Exit our for loop
        # Check left pin
        elif len(story.left_pin.controls) > 0:  # If top is empty, check left
            for obj in story.left_pin.controls[:]:
                if obj.visible == True:
                    obj.pin_location = "main"
                    story.main_pin.controls.append(obj)
                   #story.main_pin.update()
                    story.left_pin.controls.remove(obj)
                    #story.left_pin.update()
                    print("Stole from left pin")
                    break
        # Check right pin
        elif len(story.right_pin.controls) > 0:  # If top and left are empty, check right
            for obj in story.right_pin.controls[:]:
                if obj.visible == True:
                    obj.pin_location = "main"
                    story.main_pin.controls.append(obj)
                    #story.main_pin.update()
                    story.right_pin.controls.remove(obj)
                    #story.right_pin.update()
                    print("Stole from right pin")
                    break
        # Check bottom pin
        elif len(story.bottom_pin.controls) > 0:  # If top, left, and right are empty, check bottom
            for obj in story.bottom_pin.controls[:]:
                if obj.visible == True:
                    obj.pin_location = "main"
                    story.main_pin.controls.append(obj)
                    #story.main_pin.update()
                    story.bottom_pin.controls.remove(obj)
                    #story.bottom_pin.update()
                    print("Stole from bottom pin")
                    break

        # If there are no visible widgets anywhere else either
        else:
            print('No widgets visible')


    # Steal from other pins if main pin is empty. 
    # Check if empty. if yes, steal from other pins
    if len(story.main_pin.tabs) == 0:   
        steal_from_other_pins()
    # If not empty, check if any of the objects are visible
    else:
        # If all objects are invisible, steal. Otherwise do nothing
        if all(obj.visible == False for obj in story.main_pin.tabs[:]):
          steal_from_other_pins()