import glob
import os
def get_participant_list(datadir, file_wildcard):
    #get list of participant directories 
    participant_paths = glob.glob(os.path.join(datadir,'*'))

    # Initialize lists for participants with hd drum session files
    participants = []

    # Check each participant directory for session files
    for participant_path in participant_paths:
        participant = os.path.basename(participant_path)
        
        # Define the path pattern for session files for this participant
        session_paths = glob.glob(os.path.join(datadir, participant, file_wildcard))
        
        if session_paths:  # If there are any session files
            participants.append(participant)


    # Filter participant paths to include only those with session files
    participant_paths = [path for path in participant_paths if os.path.basename(path) in participants]

    # Check if we need to print or use valid_participants or filtered_participant_paths
    print("Valid Participants:", participants)
    print("Filtered Participant Paths:", participant_paths)
    return participants