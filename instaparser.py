from selenium import webdriver
import os
from platform import system
from selenium.common.exceptions import NoSuchElementException


class InstaParser:
	def __init__(self, link: str):
		self.driver = webdriver.Chrome()
		self.link = link
		try:
			self.name = self.link.split('/')[-2]
		except IndexError:
			self.name = None


	def id(self):
		try:
			self.driver.get(self.link)
			return self.name
		except:
			return 'Name does not exists'

	def info(self):
		try:
			self.driver.get(self.link)
			return self.driver.find_element_by_class_name('-vDIg').text
		except:
			return 'description does not exists'

	def activity(self):
		try:
			self.driver.get(self.link)
			return self.driver.find_element_by_class_name('k9GMp ').text
		except:
			return 'error'

	def __str__(self):
		self.driver.get(self.link)
		print(self.name)
		print('\n')
		try:
			print(self.driver.find_element_by_class_name('k9GMp ').text)
		except NoSuchElementException:
			print('Activity does not exists')
		print('\n')
		try:
			return self.driver.find_element_by_class_name('-vDIg').text
		except NoSuchElementException:
			return 'Description does not exists'


url = input('Url: ')
if 'https://www.instagram.com' in url.lower():
	human = InstaParser(url)
	print(human)

else:
	print('Invalid url')