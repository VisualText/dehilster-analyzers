import urllib.request
import os
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re

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

def fetch_names():
    urlbase = f"https://www.behindthename.com/names/"
    txt = f"all-names.dict"

    filename = os.path.join(os.path.dirname(__file__), txt)
    file1 = open(filename, "a", encoding="utf-8")
    header = f"# Most common names from all languages\n"
    file1.write(header)
    
    for i in range(1,87):
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
                nll = div.find('a', class_='nll')
                name = nll.text.lower()
                name = name.replace("-"," - ")
                name = name.replace("'"," ' ")
                name = name.replace(" 1","")
                name = name.replace(" 2","")
                name = name.replace(" 3","")
                name = name.replace(" 4","")
                name = name.replace(" 5","")

                fem = div.find('span', class_='fem')
                masc = div.find('span', class_='masc')

                dictline = name + " name=1"
                if fem and masc:
                    dictline = dictline + f" gender=mf"
                elif fem:
                    dictline = dictline + f" gender=f"
                elif masc:
                    dictline = dictline + f" gender=m"
                     
                langs = div.find_all('a', class_='usg')
                list = []
                for lang in langs:
                    ltext = lang.text.lower()
                    tokens = re.split(r'(\d+|\W+)', ltext)
                    first = tokens[0]
                    val = '1'
                    for tok in tokens:
                        if tok.lower() == 'rare':
                            val = 'rare'
                            break
                    attr = f"{first}={val}"
                    if attr not in list:
                        list.append(attr)
                        dictline = dictline + f" {attr}"
                    else:
                        moost = 1
                     
                dictline = dictline + "\n"

                print(dictline.strip())
                file1.write(dictline)

    file1.close()

# def fetch_dictionary(fem,masc,language,abbrev):
#     fetch_names(fem,language,'feminine',abbrev)
#     fetch_names(masc,language,'masculine',abbrev)

    # txt = f"{abbrev}-names.txt"
    # filename = os.path.join(os.path.dirname(__file__), txt)
    # dict = f"{abbrev}-names.dict"
    # dictname = os.path.join(os.path.dirname(__file__), dict)
    # sort_and_remove_duplicates(filename,dictname)
    # os.remove(filename)

fetch_names();
# fetch_dictionary(6,7,'arabic','ar')
# fetch_dictionary(13,5,'chinese','zh')
# fetch_dictionary(14,13,'japanese','jp')
# fetch_dictionary(10,9,'spanish','sp')
# fetch_dictionary(8,7,'portuguese','pt')
# fetch_dictionary(2,2,'tamil','ta')
# fetch_dictionary(3,3,'hindi','hi')
# fetch_dictionary(1,1,'nepali','ne')