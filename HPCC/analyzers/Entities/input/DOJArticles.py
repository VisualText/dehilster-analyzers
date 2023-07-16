import urllib.request
from bs4 import BeautifulSoup
import os
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

def read_url(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html

def write_to_file(content, filename, mode='wb'):
    with open(filename, mode) as f:
        f.write(content)
        
inputdir = os.path.dirname(os.path.realpath(__file__))
articlesXML = Element('articles')
j = 0

for i in range(1,5):
	url = f"https://www.justice.gov/news?search_api_fulltext=%20indictment&start_date=&end_date=&sort_by=field_date"
	if i > 1:
		 url = f"https://www.justice.gov/news?search_api_fulltext=%20indictment&start_date=&end_date=&sort_by=field_date&page={i}"
	print('NEW PAGE: ' + url)
	html = read_url(url)
        
	soup = BeautifulSoup(html, 'html.parser')
	articles = soup.find_all('article')

	for article in articles:
		nt = article.find('h2', class_='news-title')
		anchor = nt.find('a')
		title = anchor.text.strip()
		link = 'https://justice.gov/' + anchor['href']
		htm = read_url(link)
                
		s = BeautifulSoup(htm, 'html.parser')
		divtext = s.find_all('div', class_=lambda c: c and 'field_body' in c)
		text = divtext[0].text
		text = text.replace('\n','\n\n')
                
		artXML = SubElement(articlesXML,'article')
		titleXML = SubElement(artXML,'title')
		titleXML.text = title
		urlXML = SubElement(artXML,'url')
		urlXML.text = link
		textXML = SubElement(artXML,'text')
		textXML.text = text
        
		zero = ''
		if j < 10:
			zero = '0'
		artfile = f'{inputdir}\\articles\\DOJArticle{zero}{j}.txt';
		write_to_file(text.encode(), artfile)
		j = j + 1
	
		print('TITLE: ' + title)

xmlfile = f'{inputdir}\DOJArticles.xml'
write_to_file(tostring(articlesXML), xmlfile)
