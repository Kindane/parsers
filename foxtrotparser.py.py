import requests
from bs4 import BeautifulSoup
import os
from platform import system


def get_html(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
	r = requests.get(url, headers=hdr)
	return r.text

'''
count_of_pages = soup.find('li', class_='listing__pagination-nav').previous_sibling.previous_sibling.find('a').text
print(count_of_pages)
'''
def get_total_pages(html):
	try:
		soup = BeautifulSoup(html, 'html.parser')
		count_of_pages = soup.find('li', class_='listing__pagination-nav').previous_sibling.previous_sibling.find('a').text
		return int(count_of_pages)
	except:
		return 1


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	cards = soup.find_all('div', class_='card')
	for card in cards:
		title = card.find('a', class_='card__title').text
		price = card.find('div', class_='card-price').text
		href = card.find('div', class_='card__image').find('a').get('href')
		print(f'{title} ===> {price}, https://www.foxtrot.com.ua{href}')
	print('\n')




def main():
	url = input('Введите ссылку на категорию интерисующих вас товаров:\n')
	count_of_pages = get_total_pages(get_html(url))
	print('\n')
	pages = int(input(f'Введите количество страниц, информацию с которых вы хотите узнать\n(всего страниц {count_of_pages})\n'))
	if pages > count_of_pages:
		pages = count_of_pages
	cls()
	print('Страница №1')
	get_content(get_html(url))
	for page in range(2, pages+1):
		print(f'Страница №{page}')
		get_content(get_html(url + '?page='+ str(page)))

if __name__ == '__main__':
	print('''\nДобро пожаловать в питоноискатель 3000
Перейдите на сайт "https://www.foxtrot.com.ua/",
выберите интересующую вас категорию,
введите количество страниц и ожидайте магии :D\n''')
	try:
		main()
	except KeyboardInterrupt:
		print('Программа завершена')
	except:
		print('ОшибОчка')