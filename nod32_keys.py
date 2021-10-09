import requests
from bs4 import BeautifulSoup


hdr = {
	'User-Agent':
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}


def get_html(url):
	return requests.get(url, headers=hdr).text


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	return soup


def main():
	url = 'https://32nod.ru/'
	soup = get_content(get_html(url))
	counter = 1
	for password in soup.find_all('td', {'class': 'password', 'colspan': '2'}):
		print(counter, end='-> ')
		print(password.text)
		counter += 1


if __name__ == '__main__':
	main()
	input()
