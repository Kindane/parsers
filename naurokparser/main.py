import requests
from bs4 import BeautifulSoup
import urllib.parse


"""
url = 'https://example.com/somepage/?'

params = {'q': 'Контрольна робота Числові Послідовності', 'page': 1}
print(url + urllib.parse.urlencode(params))
"""


subjects = {
        "algebra": 1,
        "chemistry": 16,
        "physics": 2,
        "geometry": 5,
        "foreign literature": 6
        }

def main():
    url = "https://naurok.com.ua/site/search-resources?"
    print("avaliable subjects:", subjects)
    code = subjects[input("subject: ")]
    query = input("name of test: ")
    number_of_questions = int(input("number of questions: "))
    blocks_on_page = 20

    payload = {
            "q": query,
            "type[]": "test",
            "subject[0]": code,
            "page": 1
            }

    r = requests.get(url + urllib.parse.urlencode(payload))
    soup = BeautifulSoup(r.text, "lxml")
    matches = int(soup.find("div", {"class": "search-block-count"}).text.split()[1])
    number_of_pages = int(matches / blocks_on_page)
    print(number_of_pages)

    
    for i in range(number_of_pages):
        for block in soup.find_all("div", {"class": "file-item test-item"}):
            count = int(block.find("div", {"class": "testCounter"}).text)
            headline = block.find("div", {"class": "headline"})
            href = headline.find("a")

            if count == number_of_questions:
                print("https://naurok.com.ua" + href["href"])
        payload["page"] += 1
        r = requests.get(url + urllib.parse.urlencode(payload))
        soup = BeautifulSoup(r.text, "lxml")


    #path = "https://naurok.com.ua/site/search-resources?q=%D0%9A%D0%BE%D0%BD%D1%82%D1%80%D0%BE%D0%BB%D1%8C%D0%BD%D0%B0+%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%B0+%D0%A7%D0%B8%D1%81%D0%BB%D0%BE%D0%B2%D1%96+%D0%BF%D0%BE%D1%81%D0%BB%D1%96%D0%B4%D0%BE%D0%B2%D0%BD%D0%BE%D1%81%D1%82%D1%96&type%5B0%5D=test&subject%5B0%5D=1&page=2"
    #print(urllib.parse.parse_qs(path))


if __name__ == "__main__":
    main()
