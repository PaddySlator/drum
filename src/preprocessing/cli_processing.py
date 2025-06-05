import argparse
import os
import pickle
from csv_cleaner import clean_csv_files

def main():
    parser = argparse.ArgumentParser(description="Clean a single CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file to clean.")
    args = parser.parse_args()

    # Extract participant name from file path, e.g., /data/participant01/session-01-track-1.csv
    csv_path = args.csv_file
    participant = os.path.basename(os.path.dirname(csv_path))
    datadir = os.path.dirname(os.path.dirname(csv_path))  # assumes /root_dir/participant/file.csv
    file_wildcard = os.path.basename(csv_path)  # use just this file
    required_metadata_keys = ['User Id', 'Date', 'Time']

    metadata, fulldata = clean_csv_files(datadir, [participant], file_wildcard, required_metadata_keys)

    print("Done.")
    
    # Optionally: output cleaned data or summary
    input_basename = os.path.basename(args.csv_file)  # e.g., uoc01991-hd-output-device-...csv
    output_dir = r"C:\Users\lenovo\Desktop\drum-hackathon\data\clean"
    output_filename = os.path.splitext(input_basename)[0] + ".pkl"  # → .pkl
    output_path = os.path.join(output_dir, output_filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'wb') as f:
        pickle.dump({'metadata': metadata, 'fulldata': fulldata}, f)

    print(f"Saved cleaned data to: {output_path}")
    print(metadata)
    print(fulldata)
    
    # to use this pkl file, type the code below in the ipynb file
    # import pickle

    # with open("path/to/file", "rb") as f:
    #     data = pickle.load(f)

    # metadata = data["metadata"]
    # fulldata_table = data["fulldata"]

if __name__ == "__main__":
    main()
