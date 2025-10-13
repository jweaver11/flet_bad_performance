
# Called when an object is loaded. 
def verify_data(object, required_data: dict) -> bool:
    ''' Verifys an object's data has all required fields passed in '''

    # All objects will have their own data used against the passed in data to verify the dict
    #print(f"Verifying data for object {object.title}")
    #print(f"Current data: {object.data} \n")
    #print(f"Data to verify: {required_data}\n")

    # Sets our data to an empty dict if None or not a dict, so we can add to it
    if object.data is None or not isinstance(object.data, dict):
        object.data = {}


    def _verify_data(current_data: dict, required_data: dict):
        ''' Internal recursive function to verify nested dicts '''
        
        for key, value in required_data.items():
            if isinstance(value, type):
                if key not in current_data or not isinstance(current_data[key], value):
                    current_data[key] = value()
            elif isinstance(value, dict):
                if key not in current_data or not isinstance(current_data[key], dict):
                    current_data[key] = {}
                _verify_data(current_data[key], value)
            else:
                if key not in current_data:
                    current_data[key] = value
        


    try:
        _verify_data(object.data, required_data)
        # Run through the required data keys passed in, and make sure the object has it. If not, create it

        # Save our updated data back to the file
        object.save_dict()      
        return True
    
    # Catch any errors and print them
    except Exception as e:
        print(f"Error verifying data for object {object.title}: {e}")
        return False
