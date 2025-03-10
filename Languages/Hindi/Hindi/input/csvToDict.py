import os
import csv
import re

script_dir = os.path.dirname(__file__)
input_file = os.path.join(script_dir, 'hindi.csv')
output_file = os.path.join(script_dir, 'hindi.dict')

def parse_line(line):
    # Use the csv module to handle double-quoted strings and commas
    reader = csv.reader([line], quotechar='"', delimiter=',', skipinitialspace=True)
    return next(reader)[:3]  

unique_entries = set()

with open(input_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        reader = csv.reader([line], quotechar='"', delimiter=',', skipinitialspace=True)
        items = parse_line(line)
        if len(items) == 3:
            second_string = items[1]
            if not re.search(r'[ ,.;:!?(){}\[\]\/]', second_string):
                first_word = second_string
                third_string = items[2].lower()
                third_string = third_string.replace("adjective", "adj").replace("adverb", "adv")
                third_string = third_string.replace("conjunction", "conj").replace("interrogative", "inter")
                third_string = third_string.replace("intransitiveverb", "verb").replace("transitiveverb", "verb")
                third_string = third_string.replace("noundanddeterminer", "det").replace("determiner", "det")
                third_string = third_string.replace("abbreviation", "abbrev")
                
                unique_entries.add(f"{first_word} pos={third_string}")

sorted_entries = sorted(unique_entries)

with open(output_file, 'w', encoding='utf-8') as outfile:
    for entry in sorted_entries:
        outfile.write(f"{entry}\n")