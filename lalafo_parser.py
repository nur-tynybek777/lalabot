import requests
from bs4 import BeautifulSoup
import os
import csv
import json
import datetime
import sys
import time


# GLOBAL_URL = "https://lalafo.kg/kyrgyzstan/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir"
# GLOBAL_URL = "https://lalafo.kg/bishkek/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir?price[from]=500&price[to]=50000&currency=KGS"
# GLOBAL_URL = "https://lalafo.kg/bishkek/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir/3-mkr/4-mkr/5-mkr/property-host?price[from]=5000&price[to]=100000&currency=KGS"
# GLOBAL_URL = f"https://lalafo.kg/bishkek/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir/property-host?price[from]=5000&price[to]=100000&currency=KGS?page=1"

districts = ['vostok-5', 'energetiki', 'rajon-bgu', 'archa-beshik', 'ak-ordo', 'alamedin-rynok', 'ak-bosogo', 'ak-orgo', 'ala-too', 'ak-tilek', 'ak-bata', 
'altyn-ordo', 'rajon-avtorynka-azamat', 'alamedin-1', 'batken-bazar', 'p-23249-asanbaj', 'manas-airport', 'vostochnyi-avtovokzal', 'goin', '10-mkr', '1000-melochej-karpinka', 
'11-mkr', '110-kvartal', '12-mkr', '3-mkr', '4-mkr', '5-mkr', '6-mkr', '7-mkr', '8-mkr', '9-mkr', 'azija-moll', 'ak-keme-staryj-ajeroport', 'ata-tjurk-park', 'bajat-rynok-bazar', 'beta-stores', 
'beta-stores-2', 'bishkek-park-trc', 'botanicheskij-sad', 'voennyj-gorodok', 'gaz-gorodok', 'gorodok-stroitelej', 'gorodskaja-bolnica-4-ul-ajni', 'ak-zhar-zhm', 'p-30333-ak-ordo-3-zhm', 
'ala-archa-zhm', 'p-30342-ak-ordo-1-zhm', 'ak-ordo-2-zhm', 'p-30346-altyn-kazyk-zhm', 'p-30347-anar-zhm', 'p-30348-aska-tash-zhm', 'p-30349-ata-zhurt-zhm', 'p-30350-bakaj-ata-zhm', 
'p-30351-birimdik-kut-zhm', 'p-30353-bugu-jene-bagysh-zhm', 'p-30354-bugu-jene-saj-zhm', 'ala-archa-tc']

districts_names = ['Восток-5', "Энергетиков", "БГУ", "Арча-Бешик", "Ак-Ордо", "Аламединский рынок", "Ак-Босого", "Ак-Орго", "Ала-Тоо", "Ак-Тилек", "Ак-Бата", 
"Алтын-Ордо", "Авторынок 'Азамат'", "Аламедин-1", "Рынок 'Баткен'", "Асанбай", "Аэропорт 'Манас'", "Восточный автовокзал", "ГОИН", "10-мкр", "1000 мелочей", 
"11-мкр", "110-квартал", "12-мкр", "3-мкр", "4-мкр", "5-мкр", "6-мкр", "7-мкр", "8-мкр", "9-мкр", "Азия Mall", "Старый аэропорт - Ак-Кеме", "Парк 'Ата-Тюрк'", "Рынок 'Баят'", "Бета-Сторес", 
"Бета-Сторес 2", "Бишкек-Парк", "Ботанический сад", "Военный городок", "Газ Городок", "Городок строителей", "4 гор.больница", "Ак-Жар", "Ак-Ордо-3", 
"Ала-Арча", "Ак-Ордо-1", "Ак-Ордо-2", "Алтын-Казык", "Анар", "Аска-Таш", "Ата-Журт", "Бакай-Ата", "Биримдик-Кут", "Бугу-Эне-Багыш", "Бугу-Эне-Сай", "Ала-Арча ТРЦ"]

PATH = '.'

empty_dict = {'0': {'add_id': '', 'user_name': ' ', 'link': '',
		'city': '', 'currency': '', 'price': '', 'category': '',
		'mobile': '', 'description': '', 'image_url': '', 
		'created_time': '', 'updated_time': ''}}


if f'appartments.json' in os.listdir(f'{PATH}'):
	print('There is JSON file')
	with open(f'{PATH}/fresh_appartments.json', 'w', encoding='utf-8') as file:
		json.dump(empty_dict, file, indent=4, ensure_ascii=False)
else:
	print('JSON file is absence. I am creating empty file.')
	with open(f'{PATH}/appartments.json', 'w', encoding='utf-8') as file:
		json.dump(empty_dict, file, indent=4, ensure_ascii=False)

	with open(f'{PATH}/fresh_appartments.json', 'w', encoding='utf-8') as file:
		json.dump(empty_dict, file, indent=4, ensure_ascii=False)


def get_html(url):
	response = requests.get(url)
	return response


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	json_data = soup.find('script', attrs={'type':'application/json'}).get_text()
	return json_data


def get_data_lalafo(file, district):
	data = json.loads(file)
	list_of_info = data['props']['initialState']['listing']['listingFeed']['items']

	
	fresh_dict = {}
	i = 0
	for index in range(len(list_of_info)):
		temp_dict = {}
		add_id = list_of_info[index]['id']
		user_id = int(list_of_info[index]['user_id'])
		user_name = list_of_info[index]['user']['username']
		link = 'https://lalafo.kg' + (list_of_info[index]["url"])
		city = list_of_info[index]["city"]
		price = list_of_info[index]["price"]
		currency = list_of_info[index]["currency"]
		category = list_of_info[index]["ad_label"]
		mobile = list_of_info[index]['mobile']
		description = list_of_info[index]['description'].replace('\n\n', '\n')
		
		# Control agency
		if 'гентство' in user_name:
			continue

		# Control mobile phone
		try:
			image_url = list_of_info[index]['images'][0]['thumbnail_url']
		except IndexError:
			image_url = ' '

		if list_of_info[index]['mobile'] is None:
			mobile = '***'

		created_time = list_of_info[index]['created_time']
		created_time = datetime.datetime.fromtimestamp(int(created_time)).strftime('%Y-%m-%d %H:%M:%S')
		updated_time = list_of_info[index]['updated_time']
		updated_time = datetime.datetime.fromtimestamp(int(updated_time)).strftime('%Y-%m-%d %H:%M:%S')

		temp_dict[user_id] = {'add_id': add_id, 'user_name': user_name, 
		'link': link, 'city': city, 'currency': currency, 'price': price, 'category': category,
		'mobile': mobile, 'description': description, 'image_url': image_url, 
		'created_time': created_time, 'updated_time': updated_time, 'district': district}

		
		with open(f'{PATH}/appartments.json', 'r', encoding='utf-8') as file:
			prev_dict = json.load(file)

		# print('\n')
		# print(user_id, type(user_id))
		# print(temp_dict)
		# print('\n')


		for key in prev_dict:
			if int(key) == user_id:
				print(key, type(key), 'Match!')
				break
			else:
				print(key, type(key))
				fresh_dict[user_id] = {
				'add_id': temp_dict[user_id]['add_id'], 'user_name': temp_dict[user_id]['user_name'], 
				'link': temp_dict[user_id]['link'], 'city': temp_dict[user_id]['city'], 
				'currency': temp_dict[user_id]['currency'], 'price': temp_dict[user_id]['price'], 
				'category': temp_dict[user_id]['category'], 'mobile': temp_dict[user_id]['mobile'], 
				'description': temp_dict[user_id]['description'], 'image_url': temp_dict[user_id]['image_url'], 
				'created_time': temp_dict[user_id]['created_time'], 'updated_time': temp_dict[user_id]['updated_time'], 'district': temp_dict[user_id]['district']}


		double_dict = {**prev_dict, **fresh_dict}

		with open(f'{PATH}/appartments.json', 'w', encoding='utf-8') as file:
			json.dump(double_dict, file, indent=4, ensure_ascii=False)

		with open(f'{PATH}/fresh_appartments.json', 'w', encoding='utf-8') as file:
			json.dump(fresh_dict, file, indent=4, ensure_ascii=False)


def parse():
	for district in range(len(districts)):
		print(f"Parsing district - {districts[district]}")
		GLOBAL_URL = f"https://lalafo.kg/bishkek/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir/{districts[district]}/property-host?price[from]=5000&price[to]=100000&currency=KGS"
		response = get_html(GLOBAL_URL)
		if response.status_code == 200:
			html = response.text
			json_data = get_content(html)
			get_data_lalafo(json_data, districts_names[district])
		else:
			print("We've a problem with server!")
		district+=1


if __name__ == '__main__':
	parse()


