'''
This program walks through the 'Files' directory and looks for relevant .csv files, read them and count how many lines it has then store that output to a new .csv file
'''

import os
import csv
import pandas as pd

output = []

def write_to_csv():
    '''Write to new csv file
    Args: None
    Returns: None
    '''
    try:
        df = pd.DataFrame(output)
        output_file = input("Name your file or leave blank to use default name 'output.csv': ")
        output_file = output_file.strip()
        if not output_file:
            output_file = "output.csv"
        elif ".csv" not in output_file[-4:]:
            output_file += ".csv"
        output_file = f'Output/{output_file}'
        print(f'Saving file to {output_file}')
        df.to_csv(output_file, index=False)
    except IOError as e:
        print(f'Something went wrong: {e}\nPress Enter to try again')
        write_to_csv()
    except Exception as e:
        print(f'Exception found in write_to_csv(): {e}')


def read_csv(file_path, row):
    '''Read csv file
    Args:
        file_path: file path
        row: row object
    Returns:
        None
    '''
    try:
        with open(file_path, 'r') as file:
            file_object = csv.reader(file)
            row_count = sum(1 for row in file_object)
            # Subtract header (row 1)
            row['Count'] = row_count-1
            output.append(row)
    except Exception as e:
        print(f'Exception occurred in read_csv: {e}')


def main():
    '''Main method
    Args: None
    Returns: None
    '''
    try:
        # Set working directory. User can specify or it will default to local "Files" folder
        path = input("Enter directory containing data or leave blank if using local 'Files' folder: ")
        if not path.strip():
            path = "Files"
            print("Using local 'Files' directory...")
        else:
            while not os.path.exists(path):
                path = input("Please enter a valid path or leave blank to use local 'Files' folder: ")
        # Iterate through directories
        for cur_dir, sub_dirs, files in os.walk(path):
            # Current folder
            basename = os.path.basename(cur_dir)
            if "old" not in basename.lower():
                # Find .csv files
                if len(files) == 0 and not sub_dirs:
                    # No files or sub directories in present folder
                    row = {}
                    row['Folder name'] = basename
                    row['File name'] = ""
                    row['Count'] = 0
                elif len(files) == 0 and "old" in (d.lower() for d in sub_dirs):
                    # No files in present folder but contains an "OLD" sub folder
                    row = {}
                    row['Folder name'] = basename
                    row['File name'] = ""
                    row['Count'] = 0
                else:
                    for file in files:
                        row = {}
                        if file.endswith(".csv"):
                            file_path = f'{cur_dir}/{file}'
                            row['Folder name'] = basename
                            row['File name'] = file
                            read_csv(file_path, row)
        write_to_csv()
        print("COMPLETE\n")
    except Exception as e:
        print(f'Exception occurred in main: {e}')

if __name__ == "__main__":
    main()
