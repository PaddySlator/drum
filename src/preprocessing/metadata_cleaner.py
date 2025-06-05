#function to clean trailing commas from metadata
def clean_metadata(metadata):
    # Remove keys with None values directly
    keys_to_remove = [k for k, v in metadata.items() if v is None]

    for key in keys_to_remove:
        del metadata[key]
        
    # Define the fields that should not be converted
    non_convertible_fields = {
        'User Id', 'Date', 'Time', 'Session', 'Track', 
        'Track File', 'Metadata File'
    }
    cleaned_metadata = {}
    for key, value in metadata.items():
        if isinstance(value, dict):
            cleaned_value = clean_metadata(value)
        else:
            # Remove trailing commas and whitespace
            cleaned_value = value.rstrip(', ')
            
            # Convert to float if not in non_convertible_fields
            if key not in non_convertible_fields:
                try:
                    cleaned_value = float(cleaned_value)
                except ValueError:
                    print(f"Could not convert {key}: {cleaned_value} to float")
        
        # Update the cleaned_metadata dictionary
        cleaned_metadata[key] = cleaned_value
        
    return cleaned_metadata