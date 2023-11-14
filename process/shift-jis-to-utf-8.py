import os

# Directory containing the files
directory = "../yh-page/1988"

# Get all files in the directory
all_files = os.listdir(directory)
all_files = [file for file in all_files if file.endswith('.html')]

for file_name in all_files:
    file_path = os.path.join(directory, file_name)

    try:
        # Read the file in Shift-JIS encoding
        with open(file_path, 'r', encoding='shift_jis') as file:
            content = file.read()

        # Write the content in UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Converted {file_name} to UTF-8.")

    except UnicodeDecodeError:
        print(f"Error decoding {file_name}. Skipping this file.")
    except Exception as e:
        print(f"An error occurred with {file_name}: {e}")

print("Conversion process completed.")
