import csv
import sys
import os

# Add the path to the 'src' folder (adjust as needed)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing.metadata_cleaner import clean_metadata

def generate_csv_file(data):
    # Assume data is like: {('HG974d61330a861f52', 0, 1): 
    # {'User Id': '974d61330a861f52', 'Date': '2024/02/18', 'Time': '21:53:18', 'Session': '0,', 'Track': '0,', 'Track File': 'S00_Introduction From Jaime_00bpm_2-00.mp3', 'Metadata File': 'S00_Introduction From Jaime_00bpm_2-00.csv', 'Track Duration(s)': '338', 'Total Engagement Time(s)': '338.237', 'Total Drum hits in track': '0', 'Timing Window (ms)': '1000'
    
    file_path = r'C:\Users\lenovo\Desktop\drum-hackathon\data\simulated\output.csv'  # replace with your desired path and filename
    data = clean_metadata(data)
    value_dict = list(data.values())[0]
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        for key, value in value_dict.items():
            writer.writerow([key, value])

    print(f"CSV file saved to: {file_path}")

data = {('ANf47C724bf2790fb4', 7, 1): {'User Id': '3aaf316c0cf49502', 'Date': '2024/02/29', 'Time': '17:42:31', 'Session': '7,', 'Track': '0,', 'Track File': 'S06_Session 6_62bpm_1-00.mp3', 'Metadata File': 'Sess 6 CR Oct22 Midi 62bpm_2-00.csv', 'Track Duration(s)': '553', 'Total Engagement Time(s)': '553.587', 'Total Drum hits in track': '539', 'Timing Window (ms)': '200', 'Timing Window Skew (ms)': '0', 'Allowed Time Before expected hit (ms)': '100', 'Allowed Time After expected hit (ms)': '100', 'Successful Drum hits': '396', 'Success Accuracy Threshold (%)': '70', 'Average Hit Accuracy (%)': '73', 'Average Reaction Time (ms)': '34', 'Average Left Reaction time (ms)': '35', 'Average Right Reaction time (ms)': '33', 'Best Left Reaction time (ms)': '0', 'Best Right Reaction time (ms)': '0', 'Left Accuracy (%)': '69', 'Right Accuracy (%)': '77', 'Left Hit Score': '184'}}
generate_csv_file(data)