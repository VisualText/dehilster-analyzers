import urllib.request
import os
import codecs
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re

def fetch_dictionary(num, lang, gender, abbrev, charflag):
    urlbase = f"https://www.behindthename.com/submit/names/gender/{gender}/usage/{lang}/"
    dict = f"{abbrev}-names.dict"

    filename = os.path.join(os.path.dirname(__file__), dict)
    file1 = open(filename, "a", encoding="utf-8")
    
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
                if charflag != 0:
                    dictline = dictline + f" {lang}=\"{char}\""
                dictline = dictline + "\n"

                print(dictline.strip())
                file1.write(dictline)

    file1.close()

fetch_dictionary(13,'chinese','feminine','zh',1)
fetch_dictionary(5,'chinese','masculine','zh',1)
fetch_dictionary(14,'japanese','feminine','jp',1)
fetch_dictionary(13,'japanese','masculine','jp',1)
fetch_dictionary(10,'spanish','feminine','sp',0)
fetch_dictionary(9,'spanish','masculine','sp',0)
fetch_dictionary(8,'portuguese','feminine','pt',0)
fetch_dictionary(7,'portuguese','masculine','pt',0)