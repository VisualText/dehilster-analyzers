import requests
import os
from bs4 import BeautifulSoup

def fullpath(file_name, subdir=""):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "pt", "ConjugSite", "input", subdir, file_name)
    return file_path

# Read the list of words from a text file (assuming the file is named "words.txt")

input_file = fullpath("verbs.txt")
with open(input_file, "r", encoding="utf-8") as file:
    words = file.read().splitlines()

# Base URL to create the search URLs (replace with an actual search engine URL)
base_url = "https://www.conjugacao.com.br/verbo-"

# Initialize a list to store the extracted content
extracted_content = []
counter = 0
wordcount = len(words)

# Iterate over each word
for word in words:
    counter += 1
    print(f"Downloading {counter}/{wordcount} '{word}'...")
    output_file = fullpath(f"{word}.txt","words")
    if os.path.exists(output_file):
        continue

    # Create the search URL
    search_url = base_url + word

    # Send a GET request to the search URL
    response = requests.get(search_url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the div with class "content-card" (adjust the class name as needed)
    content_card_div = soup.find("div", class_="content-card")

    with open(output_file, "w", encoding="utf-8") as f:
        html = content_card_div.prettify()
        f.write(html)