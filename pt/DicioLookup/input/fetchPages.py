import requests
import os
from bs4 import BeautifulSoup
import unicodedata

def fullpath(file_name, subdir=""):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, subdir, file_name)
    # file_path = os.path.join(current_directory, "pt", "DicioLookup", "input", subdir, file_name)
    return file_path

def remove_accents(input_string):
    nfkd_form = unicodedata.normalize('NFKD', input_string)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

# Read the list of words from a text file (assuming the file is named "words.txt")

input_file = fullpath("words.txt")
with open(input_file, "r", encoding="utf-8") as file:
    words = file.read().splitlines()

# Base URL to create the search URLs (replace with an actual search engine URL)
base_url = "https://www.dicio.com.br/"

# Initialize a list to store the extracted content
extracted_content = []
counter = 0
good_counter = 0
orphan_counter = 0
wordcount = len(words)

processed_path = fullpath("processed.txt")
processed = []
if os.path.exists(processed_path):
    with open(processed_path, "r", encoding="utf-8") as file:
        processed = file.read().splitlines()
process_counter = len(processed)

orphan_file = fullpath("orphans.txt")
orphans = []
if os.path.exists(orphan_file):
    with open(orphan_file, "r", encoding="utf-8") as file:
        orphans = file.read().splitlines()
orphan_counter = len(orphans)

# orphan_new = fullpath("orphans-fixed.txt")
# with open(orphan_new, "w", encoding="utf-8") as file:
#     for o in orphans:
#         file.write(o.lower() + "\n")

# Iterate over each word
for word in words:
    counter += 1
    word = word.lower()
    output_file = fullpath(f"{word}.txt","words")
    if word in processed:
        good_counter += 1
        continue
    if word in orphans:
        continue
    print(f"Downloading {good_counter}/{orphan_counter}/{counter}/{wordcount} '{word}'...", end=" ")

    # Create the search URL
    search_url = base_url + remove_accents(word)

    # Send a GET request to the search URL
    response = requests.get(search_url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the div with class "content-card" (adjust the class name as needed)
    content_card_div = soup.find("div", class_="card-main")

    if content_card_div:
        good_counter += 1
        print("")
        with open(output_file, "w", encoding="utf-8") as f:
            html = content_card_div.prettify()
            f.write(word + "\n")
            f.write(html)
        
        # Write the word to the process file
        with open(processed_path, "a", encoding="utf-8") as process_file:
            process_file.write(word + "\n")

    else:
        orphan_counter += 1
        print(f"   ===> not in Dicio...")
        with open(orphan_file, "a", encoding="utf-8") as f:
            f.write(word + "\n")
