
# Called when an object is loaded. 
def verify_data(object, required_data: dict, tag: str=None) -> bool:
    ''' Verifys an object's data has all required fields passed in '''

    # All objects will have their own data used against the passed in data to verify the dict
    #print(f"Verifying data for object {object.title}")
    #print(f"Current data: {object.data} \n")
    #print(f"Data to verify: {required_data}\n")


    # Run through the required data keys passed in, and make sure the object has it. If not, create it
    try:
        for key, required_data_type in required_data.items():
            if key not in object.data or not isinstance(object.data[key], required_data_type):
                object.data[key] = required_data[key]()

        # Ensure we update the tag for loading purposes for objects not stored in their own files (mini widgets mostly)
        if tag is not None:
            object.data['tag'] = tag

        # Save our updated data back to the file
        object.save_dict()      
        return True
    
    except Exception as e:
        print(f"Error verifying data for object {object.title}: {e}")
        return False
