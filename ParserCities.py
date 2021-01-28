from bs4 import BeautifulSoup
import requests
import csv
from models import Cities
from app import db
class Parser:
	def __init__(self):
		self.session = requests.Session()
		self.session.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
								'Accept-Language':'ru'}

	def get_page(self):
		url = 'https://auto.drom.ru/cities/all/'
		r = self.session.get(url)
		self.parse_block(r.text)
	
	def parse_block(self,text):
		cities = {}
		soup = BeautifulSoup(text,'lxml')
		container = soup.find('div',class_='b-content b-media-cont b-media-cont_margin_huge').find('div',class_='b-selectCars b-media-cont').find_all('noscript')
		
		# print(container[84])
		for n in range(0,84):
			for i in container[n].find_all('a'):
				city = i.text 
				url = i.get('href')
				cities.update({'city':city,'url':url})
				self.write_db(cities)
	

	@staticmethod
	def write_db(cities):
		data = Cities(city=cities['city'],
					  url=cities['url'])
		db.session.add(data)
		db.session.commit()



def main():
	p = Parser()
	p.get_page()

if __name__ == '__main__':
	main()


