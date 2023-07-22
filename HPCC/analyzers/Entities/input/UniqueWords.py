import os

def read_words_from_files(folder_path):
    words = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                for line in file:
                    words.extend(line.split())
    return words

def sort_and_remove_duplicates(words):
    sorted_unique_words = sorted(set(words))
    return sorted_unique_words

def save_to_file(sorted_unique_words, output_file):
    with open(output_file, 'w') as file:
        for word in sorted_unique_words:
            file.write(word + '\n')

inputdir = os.path.dirname(os.path.realpath(__file__))
folder_path = f'{inputdir}\\studyfiles';
output_file = f'{inputdir}\\uniques.txt';

# folder_path = input("Enter the folder path containing text files: ")
# output_file = input("Enter the path for the output file: ")

words_list = read_words_from_files(folder_path)
sorted_unique_words = sort_and_remove_duplicates(words_list)
save_to_file(sorted_unique_words, output_file)

print(f"Sorted and unique words saved to '{output_file}'.")