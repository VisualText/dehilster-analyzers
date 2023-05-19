import urllib.request

def read_url(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html

def save_html(html, filename):
    with open(filename, 'wb') as f:
        f.write(html)

for i in range(1,21):
	pre = f'_0{i}'
	if i > 9:
		pre = f'_{i}'
	if i == 1:
		pre = ''
	url = f"http://www.20000-names.com/female_english_names{pre}.htm"
	print(url)
	html = read_url(url)
	if pre == '':
		pre = '_00'
	filename = f'EngFemale{pre}.html'
	print(filename)
	save_html(html, filename)