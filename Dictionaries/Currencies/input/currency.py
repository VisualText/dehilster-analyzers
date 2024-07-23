from bs4 import BeautifulSoup
import os

def add_current_path(filename):
    current_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_path, filename)
    return full_path

# Example usage
filename = 'currencies.html'
full_path = add_current_path(filename)

# Read the HTML file
with open(full_path, 'r', encoding='utf-8') as file:
    html_text = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_text, 'html.parser')

# Find the table and extract the rows
table = soup.find('table')
rows = table.find_all('tr')

# Prepare the lines for the output file
lines = []
for row in rows:
    columns = row.find_all('td')
    line = ''
    for i, column in enumerate(columns):
        if i == 0:
            line += columns[4].text.strip() + ' '
        if i == 1:
            line += ' currency="' + columns[2].text.strip() + '" '
        if i == 2:
            line += ' code=' + columns[3].text.strip() + ' '
        if i == 3:
            line += ' country="' + columns[1].text.strip() + '"'
    lines.append(line.strip())

# Write the lines into the output file
with open('currencies.dict', 'w', encoding='utf-8') as file:
    file.write('\n'.join(lines))