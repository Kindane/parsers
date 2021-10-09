import requests
from bs4 import BeautifulSoup

def get_url(url):
	r = requests.get(url)
	return r.text

def get_soup(html):
	soup = BeautifulSoup(html, 'html.parser')
	return soup

def get_pages(soup):
	pages = []
	for page in soup.find_all('a', itemprop='url'):
		pages.append('https://zastavok.net' + str(page.get('href')))
	return pages

def parse(soup):
	img = soup.find('img', id='target')
	return 'https://zastavok.net' + img.get('src')

def get_content(url):
	return get_soup(get_url(url))



def main():
	print('''\nДобро пожаловать в скачиватель фотографий 3000!
Перейдите на сайт: "https://zastavok.net/",  выберите интересующую вас категорию,
Вставьте в консоль ссылку на страницу с жанром, а затем введите количество страниц,
с которых вы хотите скачать фотографии\n''')
	url = input('Введите ссылку: ')
	count = int(input('Введите количество страниц: '))
	for page in get_pages(get_content(url)):
		img = parse(get_content(page))
		r = requests.get(img, stream=True)
		with open(img.split('/')[-1], 'wb') as file:
			for chunk in r.iter_content(8092):
				file.write(chunk)
	print('Страница №1 спарсена удачно!', end='')
	for i in range(2, count+1):
		for page in get_pages(get_content(url + str(i) + '/')):
			img = parse(get_content(page))
			r = requests.get(img, stream=True)
			with open(img.split('/')[-1], 'wb') as file:
				for chunk in r.iter_content(8092):
					file.write(chunk)
		print('\b' * (len(str(i)) + 27), end='')
		print(f'Страница №{i} спарсена удачно!', end='')
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
	except:
		print('Ошибка')