import os
import shutil
import re

# Directory containing the files
directory = "../yh-page/raw"  # Replace with your directory path

# Get all files in the directory
all_files = os.listdir(directory)

# Regular expression pattern for matching filenames
pattern = r'^(\d{4})\d{4}\.html$'

for file_name in all_files:
    match = re.match(pattern, file_name)
    if match:
        year = match.group(1)
        year_folder = os.path.join(directory, year)

        # Create a folder for the year if it doesn't exist
        if not os.path.exists(year_folder):
            os.makedirs(year_folder)

        # Move the file into the year folder
        shutil.move(os.path.join(directory, file_name), os.path.join(year_folder, file_name))

print("Files moved successfully.")
