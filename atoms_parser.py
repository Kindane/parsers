import requests
from bs4 import BeautifulSoup

hdr = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}



def get_content(html):
	return BeautifulSoup(html, 'html.parser')


class Atoms:
	profile = 'https://atoms.com.ua/Profile/'
	my_class = 'https://atoms.com.ua/Students/'
	main_page = 'https://atoms.com.ua/'

	def __init__(self, login: str, password: str):
		self.__login = login
		self.__password = password
		self.ses = self._autorization(login, password)

	@staticmethod
	def _autorization(phone, password):
		post_url = 'https://atoms.com.ua/system/core/auth/ajax.php'
		data = {
			'act': 'login',
			'username': phone,
			'password': password,
			'remember-me': 'remember-me'}
		ses = requests.Session()
		ses.headers.update(hdr)
		for _ in range(2):
			response = ses.post(post_url, data=data).json()
			if response['status'] == 'ok':
				continue
			else:
				raise ValueError('Incorrect login or password')
		return ses

	def _get_page(self, url):
		return self.ses.get(url, headers=hdr)

	def collect_students(self):
		page = self._get_page(self.my_class)
		soup = get_content(page.text)
		list_of_students = list()
		for student in soup.findAll('b', class_='mainText'):
			student_name = student.text
			list_of_students.append(student_name)
		return list_of_students

	# Doesn't work right
	def timetable(self):
		page = self._get_page(self.main_page)
		soup = get_content(page.text)
		lessons = list()
		teachers = list()
		for lesson in soup.findAll('div', class_='btn-group on-default'):
			text = lesson.text.strip()
			lesson = text.split('\n')[0]
			teacher = text.split('\n')[3]  # i don't know why 3, but this works
			lessons.append(lesson)
			teachers.append(teacher)

		return lessons, teachers

	def get_me(self):
		page = self._get_page(self.profile)
		soup = get_content(page.text)
		name = soup.find('h3').text.strip()
		avatar = soup.find('img', id='avatar').get('src')
		avatar = 'https://atoms.com.ua/' + avatar
		coins = soup.find('b', id='coinssum').text
		return {'Name': name, 'Coins': coins, 'Avatar': avatar}


def main():
	phone = input("Phone: ")
	password = input("Password: ")
	user = Atoms(phone, password)
	print(user.get_me())


if __name__ == '__main__':
	main()
