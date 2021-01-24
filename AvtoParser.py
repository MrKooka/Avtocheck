from bs4 import BeautifulSoup
import requests
import csv
from peewee import *


db = MySQLDatabase('avto', user='root', password='1',
                         host='localhost', port=27017)

#Создаем таблицу в бд 
class Avto(Model):
	name = CharField()
	price = CharField()
	transmission = CharField()
	drive_unit = CharField()
	engen = CharField()
	type_engen = CharField()
	url = TextField()
	year = CharField()
	city = TextField()

	class Meta:
		database = db

class AvitoParser:
	def __init__(self):
		self.session = requests.Session()

		self.session.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
								'Accept-Language':'ru'}

	def get_page(self,page):
		url = 'https://togliatti.drom.ru/auto/all/page{page}/'.format(page=page)
		r = self.session.get(url)
		self.get_blocks(r.text)

	def get_blocks(self,text):
		soup = BeautifulSoup(text,'lxml')
		
		# Запрос CSS-селектора , состоящего из множества классов, производится через select
		container = soup.find('div',class_='css-imk91o ed5wxk93').find_all('a',class_='css-1hgk7d1 eiweh7o2')
		

		for item in container:	
			block = self.parse_block(item=item)
		
		# div = soup.find('div',class_='css-imk91o ed5wxk93').find('div',class_='css-1xaekgw e93r9u20')
		# self.get_page_2(div)
		

	
	def parse_block(self,item):
		
		if item.find('div',class_='css-t8t67s e6dhr4f1').find('span').text != None:
			try:
				name = item.find('div',class_='css-t8t67s e6dhr4f1').find('div',class_='css-19e84ej eozdvfu0').find('span').text.split(',')[0]
			except:
				name=''
			try:
				year = item.find('div',class_='css-t8t67s e6dhr4f1').find('div',class_='css-19e84ej eozdvfu0').find('span').text.split(',')[1]
			except:
				year = ''
			try:
				price = item.find('div',class_='css-1r6p0wr e6dhr4f2').find('div',class_='css-1dca0vj e1lm3vns0').find('span').text.strip().replace('q','')
			except:
				price=''
			try:
				engen=item.find_all('span',class_='css-1vlap19 e162wx9x0')[0].text.split(' ')[0]
			
			except:
				engen= ''

			try:
				type_engen = item.find_all('span',class_='css-1vlap19 e162wx9x0')[1].text.replace(',', '').strip()
			except:
				type_engen=''
			try:
				transmission = item.find_all('span',class_='css-1vlap19 e162wx9x0')[2].text.replace(',', '').strip()
			except:
				transmission=''
			try:
				drive_unit = item.find_all('span',class_='css-1vlap19 e162wx9x0')[3].text.replace(',', '').strip()
			except:
				drive_unit=''
			try:
				city = item.find('div',class_='css-1r6p0wr e6dhr4f2').find('div',class_='css-kakl8e e162wx9x0').find('span').text
			except:
				city = ''
			try:
				url = item.get('href')
			except:
				url = ''
			

			data = {'name':name,
					'price':price,
					'transmission':transmission,
					'drive_unit':drive_unit,
					'engen':engen,
					'type_engen':type_engen,
					'url':url,
					'city':city,
					'year':year
					}	
			self.write_db(data)
			
			return None 

	@staticmethod
	def write_db(data):
		car = Avto.create(name=data['name'],
						  price=data['price'],
						  transmission=data['transmission'],
						  drive_unit = data['drive_unit'],
						  engen = data['engen'],
						  type_engen = data['type_engen'],
						  url = data['url'],
						  city = data['city'],
						  year = data['year'])
		car.save()
	# def get_page_2(self,div):
	# 	pages = div.find('div',class_='css-se5ay5 e1lm3vns0')
	# 	for i in pages:
	# 		print(i)
	# @staticmethod
	# def write_csv(data):
	# 	with open('avto.csv', 'a') as f:
	# 		order=['name','price','transmission','drive_unit','engen','engen','type_engen','url','city','year']
	# 		writer = csv.writer(f,delimiter=';')
	# 		writer.writerow((data['name'],
	# 						data['price'],
	# 						data['transmission'],
	# 						data['drive_unit'],
	# 						data['engen'],
	# 						data['type_engen'],
	# 						data['url'],
	# 						data['city'],
	# 						data['year']))	
def main():
	p = AvitoParser()
	for i in range(1,5):
		p.get_page(i)
		print(i)
	

if __name__ == '__main__':
	main()
