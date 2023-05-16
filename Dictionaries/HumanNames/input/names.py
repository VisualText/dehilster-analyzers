import urllib.request
import os
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def sort_and_remove_duplicates(input_file, output_file):
    lines = set()  # Use a set to store unique lines
    
    # Read input file and collect unique lines
    with open(input_file, 'r', encoding="utf-8") as file:
        for line in file:
            lines.add(line.strip())
        file.close()

    # Sort the lines alphabetically
    sorted_lines = sorted(lines)
    
    # Write sorted lines to the output file
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write('\n'.join(sorted_lines))
        file.close()

def fetch_gender(num, lang, gender, abbrev):
    urlbase = f"https://www.behindthename.com/submit/names/gender/{gender}/usage/{lang}/"
    txt = f"{abbrev}-names.txt"

    filename = os.path.join(os.path.dirname(__file__), txt)
    file1 = open(filename, "a", encoding="utf-8")
    biglang = lang.capitalize();
    header = f"# {biglang} first names with gender\n"
    file1.write(header)
    
    end = num + 1
    for i in range(1,end):
        url = urlbase
        if (i > 1):
            url = f"{urlbase}{i}"
        print(url)

        try:
            page = urllib.request.urlopen(url)
        except HTTPError as e:
            print(' Error code: ', e.code)
        except URLError as e:
            print('Reason: ', e.reason)
        else:
            found = True
        
        if found == True:
            pagehtml = page.read()
            soup = BeautifulSoup(pagehtml, 'html.parser')
            div_elements = soup.find_all('div', class_='browsename')

            for div in div_elements:
                nlls = div.find_all('a', class_='nll')
                name = '';
        
                for nll in nlls:
                    name = nll.text.lower()
                    break

                trans = div.find_all('span', class_='listtrans')
                char = ''
        
                for tran in trans:
                    char = tran.text
                    break

                dictline = f"{name} name=first gender={gender}"
                if len(char) > 0:
                    dictline = dictline + f" {lang}=\"{char}\""
                else:
                    dictline = dictline + f" {lang}=1"
                dictline = dictline + "\n"

                print(dictline.strip())
                file1.write(dictline)

    file1.close()

def fetch_dictionary(fem,masc,language,abbrev):
    fetch_gender(fem,language,'feminine',abbrev)
    fetch_gender(masc,language,'masculine',abbrev)

    txt = f"{abbrev}-names.txt"
    filename = os.path.join(os.path.dirname(__file__), txt)
    dict = f"{abbrev}-names.dict"
    dictname = os.path.join(os.path.dirname(__file__), dict)
    sort_and_remove_duplicates(filename,dictname)
    os.remove(filename)

fetch_dictionary(13,5,'chinese','zh')
fetch_dictionary(14,13,'japanese','jp')
fetch_dictionary(10,9,'spanish','sp')
fetch_dictionary(8,7,'portuguese','pt')
fetch_dictionary(2,2,'tamil','ta')
fetch_dictionary(3,3,'hindi','hi')
fetch_dictionary(1,1,'nepali','ne')