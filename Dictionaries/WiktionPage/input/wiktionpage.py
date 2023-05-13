import urllib.request
import os
import codecs
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re

wordsfile = os.path.join(os.path.dirname(__file__), "test.txt")
file1 = codecs.open(wordsfile, "r", "utf-8")
lines = file1.readlines()

urlbase = "https://en.wiktionary.org/w/index.php?title="
urlsuffix = "&action=edit"
  
count = 0
for word in reversed(lines):
    word = word.strip()
    wiktionfile = os.path.join(os.path.dirname(__file__), "demo", word + ".txt")
    print(word, end =" ")

    if os.path.exists(wiktionfile):
        print (' exists')
        continue

    url = urlbase + word + urlsuffix;
    found = False

    try:
        page = urllib.request.urlopen(url)
    except HTTPError as e:
        print(' Error code: ', e.code)
        file1 = open(os.path.join(os.path.dirname(__file__), "wikophans.txt"), "a")
        file1.write(word + "\n")
        file1.close()
    except URLError as e:
        print('Reason: ', e.reason)
    else:
        found = True
    
    if found == True:
        pagehtml = page.read()
        soup = BeautifulSoup(pagehtml, 'html.parser')
        wiktion_page = soup.find('textarea')

        if wiktion_page:
            pagetext = wiktion_page.text
            if pagetext:
                print(' DOWNLOADED')
                file = codecs.open(wiktionfile, "w", "utf-8")
                file.write(word + '\n' + pagetext)
                file.close()
            else:
                print(' <=== Not in dictionary')
                file1 = open(os.path.join(os.path.dirname(__file__), "noentry.txt"), "a")
                file1.write(word + "\n")
                file1.close()
        
        else:
            print(' no defs')
            file2 = open(os.path.join("input","nopages.txt"), "a")
            file2.write(word + "\n")
            file2.close()