from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

import requests
from bs4 import BeautifulSoup

from time import sleep
import re
import sqlite3
from sqlite3 import IntegrityError


phone_regex = re.compile(r'''(
(\+?38 | \+?380 | \(\+?380\) | \(\+?38\))? # country code
(\d{3} | \(\d{3}\))               # first 3 digits
(\d{3})               # and 3 digits
(\d{4} | \d{3})               # last 4 digits
)''', re.VERBOSE)

# 380067123456
# 38 093 027 68
# 380 930 2768
# 380 953 123456


# return html of this page
def get_html(url):
	return requests.get(url).text


# return soup object of html
def get_soup(html):
	return BeautifulSoup(html, 'html.parser')


# return all_links in main page of url
def get_content(soup):
	links = set()
	ads = soup.find_all(
		'a', class_='marginright5 link linkWithHash detailsLink')
	for ad in ads:
		links.add(ad.get('href'))
	return links


# if number is good: yield number else None
def check_numbers(numbers):
	for text in numbers:
		number = ''
		for groups in phone_regex.findall(text):
			number += ' '.join([groups[2], groups[3], groups[4]])
		if number:
			if len(number) < 14:
				yield number
			else:
				print(f'Wrong phone number is: {number}')
				yield None


# open browser and search number in page.
# this funcrion is return :check_numbers: function
def start_parsing(link):
	driver = webdriver.Chrome()
	driver.get(link)
	try:
		button = driver.find_element_by_xpath(
			'//*[@id="contact_methods"]/li[2]/div/strong')
		button.click()
		sleep(0.8)
		numbers = button.text.replace(
			' ', '').replace(
			'-', '').replace(
			'(', '').replace(
			')', '').split('\n')
		return check_numbers(numbers)
	except NoSuchElementException:
		print('NoSuchElementException')
	except ElementClickInterceptedException:
		print('ElementClickInterceptedException')
	finally:
		driver.quit()


# if number not in database: insert and print
# else: print(Value already in database)
def insert_and_print(value, db, cursor):
	try:
		cursor.execute('INSERT INTO phoneNumber VALUES(?)', [value])
		db.commit()
		print(f'{value} successfully added to the database')
	except IntegrityError:
		print(f'{value} already in database')


# this function checks the value for None
def check_number(number, db, cursor):
	if number is not None:
		insert_and_print(number, db, cursor)
	else:
		print('Something wrong with phone number')


# connect to database, return tuple
def connect_to_db():
	db = sqlite3.connect('phoneNumbers.db')
	cursor = db.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS phoneNumber(numb TEXT UNIQUE)')
	db.commit()
	return (db, cursor)


# this function, using a loop, goes through all the numbers returned by the function
# checks them and writes to the database
def start_process(url, db, cursor):
	for link in get_content(get_soup(get_html(url))):
		for number in start_parsing(link):
			check_number(number, db, cursor)


# this is the main function in which the main process takes place
def main():
	# url = 'https://www.olx.ua/nedvizhimost/doma/'
	url = input('url: ')
	db, cursor = connect_to_db()
	start_process(url, db, cursor)
	for page in range(2, 5):
		start_process(url + '?page=' + str(page), db, cursor)


# Runs the main function if the file was run from the console
if __name__ == '__main__':
	main()
