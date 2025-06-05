import os
import glob
import re
import pandas as pd
import io
from collections import defaultdict

def extract_track_number(text):
    pattern = r'track-(\d+)'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return None # or handle the case when no match is found
        
def extract_session_number(filename):
    pattern = r'session-(\d+)-track'
    match = re.search(pattern, filename)
    if match:
        return int(match.group(1))
    return None

#function for reading the csv files while dealing with the metadata
def read_csv_with_metadata(csv_file, required_metadata_keys):
    """
    Reads the CSV file, checks if it contains the required metadata,
    and returns the metadata and data table if valid.
    """
    metadata = {}
    try:
        # Read metadata
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            for line in lines[:25]: # assuming metadata is in the first 25 lines
                if line.strip(): # ignore empty lines
                    try:
                        key, value = line.strip().split(',', 1)
                        metadata[key.strip()] = value.strip()
                    except ValueError:
                        # Skip lines that don't contain metadata in the expected format
                        continue
                    
            # Validate metadata
            if not all(key in metadata for key in required_metadata_keys):
                print(f"Required metadata missing in file {csv_file}")
                return None, None # Return None if required metadata is missing
            
            # Read data table
            data_lines = lines[27:] # assuming data table starts from line 27
            
            # Create DataFrame for data table
            data_table = pd.read_csv(io.StringIO(''.join(data_lines)))
            return metadata, data_table
    except Exception as e:
        print(f"Error reading file {csv_file}: {e}")
        return None, None # Return None if there is an error

# Function to filter out files starting with "~$" (temp office files)
def is_valid_file(file_path):
    return not os.path.basename(file_path).startswith('~$')

def clean_csv_files(datadir, participants, file_wildcard, required_metadata_keys):
    if required_metadata_keys is None:
        required_metadata_keys = ['User Id', 'Date', 'Time']

    metadata = defaultdict(dict)
    fulldata_table = defaultdict(dict)

    for participant in participants:
        print(f"Processing participant: {participant}")
        
        # Get the file paths to the session CSV files
        session_paths = glob.glob(os.path.join(datadir, participant, file_wildcard))
        
        # Filter out files starting with "~$"
        session_paths = [path for path in session_paths if is_valid_file(path)]
        
        # Order them so that the files are in the order they were attempted
        session_paths = sorted(session_paths)
        
         # Dictionary to track attempt numbers for each session
        session_attempt_counter = defaultdict(int)

        for session in session_paths:
            this_session_number = extract_session_number(session)
            
            # Increment the attempt number for this session
            session_attempt_counter[this_session_number] += 1
            this_attempt_number = session_attempt_counter[this_session_number]

            try:
                # Read metadata and data table
                this_metadata, this_data_table = read_csv_with_metadata(session, required_metadata_keys)
                
                if this_metadata is None or this_data_table is None: # Skip empty data
                    continue
                
                # Store metadata and data table
                metadata[(participant, this_session_number, this_attempt_number)] = this_metadata
                fulldata_table[(participant, this_session_number, this_attempt_number)] = this_data_table
                print(f"Processed participant: {participant}, session: {this_session_number}, attempt: {this_attempt_number}")
            except Exception as e:
                print(f"Error processing file {session}: {e}")

    return metadata, fulldata_table
