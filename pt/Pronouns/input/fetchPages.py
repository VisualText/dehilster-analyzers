import requests
import os
from bs4 import BeautifulSoup

def fullpath(file_name, subdir=""):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "pt", "Pronouns", "input", subdir, file_name)
    return file_path

def findHeader(tabpos):
    counter = 0
    for h in hpos:
        if h > tabpos:
            if counter == 0:
                return counter
            return counter - 1
        counter += 1
    return -1

search_url = "https://www.fluentu.com/blog/portuguese/portuguese-pronouns/"
response = requests.get(search_url)

soup = BeautifulSoup(response.content, "html.parser")

tables = soup.find_all("table", class_="tablepress")
headers = soup.find_all("h3")

htmlstr = soup.prettify()
lines = htmlstr.split("\n")

position = 0
tpos = []
for line in lines:
    lin = line.strip()
    if "tablepress" in line and not lin.startswith("<link"):
        tpos.append(position)
    position += len(line) + 1

position = 0
hpos = []
for line in lines:
    if "<h3>" in line:
        hpos.append(position)
    position += len(line) + 1

output_file = fullpath("prounouns.html")
with open(output_file, "w", encoding="utf-8") as f:
    for table in tables:
        tabpos = tpos.pop(0)
        headerpos = findHeader(tabpos)
        header = headers[headerpos].prettify()
        tableHTML = table.prettify()
        f.write(header)
        f.write(tableHTML)