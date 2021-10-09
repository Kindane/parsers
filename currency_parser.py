import requests
from bs4 import BeautifulSoup


#This code is suck

def get_html(url):
	r = requests.get(url)
	return r.text

def translate_html_to_soup(html):
	soup = BeautifulSoup(html, 'html.parser')
	return soup

def get_page_content(soup):
	c = 1
	for tr in soup.find('tbody'):
		for value in tr.find_all('span', class_='value'):
			print(tr.find('th').text, end=' ')
			if c % 3 == 0:
				print('(НБУ) = ', end=' ')
				c = 0
			elif c % 2 == 0:
				print('(Продажа) = ', end=' ')
			elif c % 1 == 0:
				print('(Покупка) = ', end=' ')
			print(value.text[:7])
			c += 1
		print('\n')


def main():
	url = 'https://finance.i.ua/'
	get_page_content(translate_html_to_soup(get_html(url)))



if __name__ == '__main__':
		main()