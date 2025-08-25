''' Handler function for arranging our story object (widgets) to their correct pin locations '''

from models.user import user
import flet as ft


# Called at the start of the by the 'render_widgets' function.
def arrange_widgets():

    print("arrange widgets called")
    
    # Called later in the function when an objects 'pin_location' is not the same as its actual reference location
    def update_pin_location(obj):
        if not hasattr(obj, 'data') or not obj.data:
            return  # Skip objects without data
        
        pin_location = obj.data['pin_location']

        # Appends the new pointer to our correct pin location
        if pin_location == "top":
            user.active_story.top_pin.controls.append(obj)
        elif pin_location == "left":
            user.active_story.left_pin.controls.append(obj)
        elif pin_location == "main":
            user.active_story.main_pin.controls.append(obj)
        elif pin_location == "right":
            user.active_story.right_pin.controls.append(obj)
        elif pin_location == "bottom":
            user.active_story.bottom_pin.controls.append(obj)

    # Check our 5 pin locations, and if objects pin locations don't match their actual location, update/move them
    # Top
    for obj in user.active_story.top_pin.controls[:]:  # Use slice to avoid modifying list while iterating
        if hasattr(obj, 'data') and obj.data and obj.data['pin_location'] != "top":  # Check if pin_location does not match its actual location
            user.active_story.top_pin.controls.remove(obj)  # Remove from top pin if not matching
            update_pin_location(obj)    # Add it to the correct pin location
    # Left
    for obj in user.active_story.left_pin.controls[:]:
        if hasattr(obj, 'data') and obj.data and obj.data['pin_location'] != "left":
            user.active_story.left_pin.controls.remove(obj)
            update_pin_location(obj)
    # Main
    for obj in user.active_story.main_pin.controls[:]:
        if hasattr(obj, 'data') and obj.data and obj.data['pin_location'] != "main":
            user.active_story.main_pin.controls.remove(obj)
            update_pin_location(obj)
    # Right
    for obj in user.active_story.right_pin.controls[:]:
        if hasattr(obj, 'data') and obj.data and obj.data['pin_location'] != "right":
            user.active_story.right_pin.controls.remove(obj)
            update_pin_location(obj)
    # Bottom
    for obj in user.active_story.bottom_pin.controls[:]:
        if hasattr(obj, 'data') and obj.data and obj.data['pin_location'] != "bottom":
            user.active_story.bottom_pin.controls.remove(obj)
            update_pin_location(obj)

    # Called when main pin is empty or has no visible widgets. (May phase out later??)
    def steal_from_other_pins():
        ''' Steals widget one widget from other pin locations and adds it to the main pin location '''

        print("steal from other pins called")

        # If pin is NOT empty. Pin's can hold widgets that are not visible, so we check that as well
        # Top
        if len(user.active_story.top_pin.controls) > 0:     # Pin has at least one widget
            for obj in user.active_story.top_pin.controls[:]:  
                if obj.visible == True and hasattr(obj, 'data') and obj.data:     # If at least one of the widgets is visible and has data

                    # Update pin location and give it a new reference in new main pin location
                    obj.data['pin_location'] = "main"   
                    update_pin_location(obj) 

                    # Remove the old reference from the old pin
                    user.active_story.top_pin.controls.remove(obj)  # Remove from top pin

                    # Exit our for loop, so it only does it to one widget, not all of them
                    print("Stole from top pin")
                    break   
        # Left
        elif len(user.active_story.left_pin.controls) > 0: 
            for obj in user.active_story.left_pin.controls[:]:
                if obj.visible == True and hasattr(obj, 'data') and obj.data:

                    obj.data['pin_location'] = "main"
                    update_pin_location(obj) 

                    user.active_story.left_pin.controls.remove(obj)
                    
                    print("Stole from left pin")
                    break
        # Right
        elif len(user.active_story.right_pin.controls) > 0:  # If top and left are empty, check right
            for obj in user.active_story.right_pin.controls[:]:
                if obj.visible == True and hasattr(obj, 'data') and obj.data:

                    obj.data['pin_location'] = "main"
                    update_pin_location(obj) 

                    user.active_story.right_pin.controls.remove(obj)
                    
                    print("Stole from right pin")
                    break
        # Bottom
        elif len(user.active_story.bottom_pin.controls) > 0:  # If top, left, and right are empty, check bottom
            for obj in user.active_story.bottom_pin.controls[:]:
                if obj.visible == True and hasattr(obj, 'data') and obj.data:
                    obj.data['pin_location'] = "main"
                    update_pin_location(obj) 

                    user.active_story.bottom_pin.controls.remove(obj)
                    
                    print("Stole from bottom pin")
                    break

        # If there are no visible widgets anywhere else either
        else:
            print('No widgets visible')


    # Steal from other pins if main pin is empty. 
    # Check if empty. if yes, steal from other pins
    if len(user.active_story.main_pin.controls) == 0:   
        steal_from_other_pins()

    # If not empty, check if any of the objects are visible
    else:

        # If all objects are invisible, steal. Otherwise do nothing
        if all(obj.visible == False for obj in user.active_story.main_pin.controls[:]):
          steal_from_other_pins()


    # Called when we have an object with no reference in any pin
    def add_object_to_pin(obj):
        print("add object to pin called")

        # Check objects pin and that its not already in that pin
        if hasattr(obj, 'data') and obj.data:  # If it has data
            if obj.data['pin_location'] == "top" and obj not in user.active_story.top_pin.controls:
                user.active_story.top_pin.controls.append(obj)
            elif obj.data['pin_location'] == "left" and obj not in user.active_story.left_pin.controls:
                user.active_story.left_pin.controls.append(obj)
            elif obj.data['pin_location'] == "main" and obj not in user.active_story.main_pin.controls:
                user.active_story.main_pin.controls.append(obj)  
            elif obj.data['pin_location'] == "right" and obj not in user.active_story.right_pin.controls:
                user.active_story.right_pin.controls.append(obj)
            elif obj.data['pin_location'] == "bottom" and obj not in user.active_story.bottom_pin.controls:
                user.active_story.bottom_pin.controls.append(obj)
        elif hasattr(obj, 'data'):  # If it has data attribute but data is None or missing pin_location
            print("Object has no pin location data, setting to main")
            if obj.data is None:
                obj.data = {}  # Initialize data if it's None
            obj.data['pin_location'] = "main"
            user.active_story.main_pin.controls.append(obj)

    
    # Checks all our objects (widgets) to check if they are in a pin or not. If not, add them to their pin location
    for char in user.active_story.characters:
        add_object_to_pin(char)
    if user.settings is not None: 
        add_object_to_pin(user.settings)

