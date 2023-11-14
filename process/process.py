from bs4 import BeautifulSoup
import os
from datetime import datetime
import re

# Directory containing the HTML files
year = "1984"
directory = "../yh-page/" + year

# Get all files in the directory
all_files = os.listdir(directory)

# Filter out only HTML files
html_files = [file for file in all_files if file.endswith('.html')]

# List to store file names and their corresponding dates
file_dates = []

def extract_date(title):
    # Extract the date from the title
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日付', title)
    if match:
        year, month, day = map(int, match.groups())
        return datetime(year, month, day)
    return None

def clear_table_attributes(table):
    # Remove attributes from table, tr, and td tags
    for tag in table.find_all(['table', 'tr', 'td']):
        tag.attrs = {}

for file_name in html_files:
    with open(os.path.join(directory, file_name), "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.text if title_tag else "No Title"
        date = extract_date(title)
        if date:
            file_dates.append((file_name, title, date))

# Sort the files based on extracted dates
file_dates.sort(key=lambda x: x[2])

# Create an empty string to hold the entire HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Charts - {year}</title>
        <link rel="stylesheet" href="../style.css">
    </head>
    <body>
        <header>
        <h1><a href="../index.html">Oricon Weekly Charts</a> - {year}</h1>
"""

# Initialize the navigation element
nav_links = "<nav><ul>\n"

# Generate navigation links
for _, title, _ in file_dates:
    nav_links += f"<li><a href='#{title}'>{title}</a></li>\n"

# Close the navigation element
nav_links += "</ul></nav>\n"

# Append the navigation links at the beginning of the body
html_content += nav_links

html_content += """
    </header>
    <hr />
"""

# Generate sections
for file_name, title, _ in file_dates:
    with open(os.path.join(directory, file_name), "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        table = soup.find("table")
        if table:
            clear_table_attributes(table)
            html_content += f"<section id='{title}'>\n"
            html_content += f"<h2>{title}</h2>\n"
            html_content += "<h3>シングルTOP20</h3>\n"
            html_content += str(table)
            html_content += "</section>\n"

# End the HTML structure
html_content += """
    <hr />

    <footer>
        <p>Reference: <a href="http://mgyh0906.web.fc2.com/oricon.html">YHの音楽とゲームのページ / オリコンチャート</a></p>
        <p>Website generated by <a href="https://scchan.moe">scchan.moe</a> | <a href="https://github.com/sichengchen/oricon-charts">GitHub</a></p>
    </footer>

</body>
</html>
"""

# Create a BeautifulSoup object with the entire content
final_soup = BeautifulSoup(html_content, 'html.parser')

# Open a new file to write the formatted website
directory = f"../public/{year}"
if not os.path.exists(directory):
    os.makedirs(directory)

with open(f"{directory}/index.html", "w", encoding='utf-8') as compiled_file:
    # Write the prettified HTML to the file
    compiled_file.write(final_soup.prettify())

print("Website compiled successfully.")
