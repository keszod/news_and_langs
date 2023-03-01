 # -*- coding: utf8 -*-
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import re
import os
import csv
import traceback
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

from time import sleep
from bs4 import BeautifulSoup as bs

def create_driver(headless=True):
	options = uc.ChromeOptions()
	options.headless=headless
	options.add_argument("--window-size=1920,1080")
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--allow-running-insecure-content')
	options.add_argument('--headless')

	driver = uc.Chrome(use_subprocess=True, options=options)

	return driver

def get_sites():
	with open('sites.txt','r',encoding='utf-8-sig') as file:
		return file.read().splitlines()

def sort_data():
	with open('not sort.txt','r',encoding='utf-8-sig') as file:
		data = file.read().splitlines()

	with open('sites.txt','a+',encoding='utf-8-sig') as file:
		for el in data:
			file.write(el.split()[0]+'\n')

def csv_pack(name,params,mode='a+'):	
	with open(name + '.csv',mode,newline='',encoding='utf-8-sig') as file:
		writer = csv.writer(file,delimiter=';')
		writer.writerow(params)


def check_if_news():
	sites = get_sites()
	driver = create_driver()
	count = 0

	for site in sites:
		try:
			if count == 15:
				count = 0
				driver.close()
				driver = create_driver()

			if not 'https://' in site:
				site = 'https://'+site
			print(site)
			driver.get(site)
			sleep(2)
			for i in range(15):
				soup = bs(driver.page_source,'html.parser')
				links = len(soup.findAll('a'))

				all_dates = re.findall('2006|2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021|2022|2023|2024',soup.text)
				dates = len(all_dates)

				if dates > 0:
					all_dates = list(filter(lambda x: x!='',all_dates))
					all_dates = list(map(lambda x: int(x),all_dates))
					
					last_date = str(max(all_dates))
				else:
					last_date = ''

				if_news_in_text = 'news' in soup.text.lower()
				
				print('Cайт',links,dates,if_news_in_text)
				
				if links > 5:
					sleep(2)
					print('Загружен')
					break
				sleep(1)

			csv_pack('result',[site,links,dates,if_news_in_text,last_date])

			count += 1
		except:
			traceback.print_exc()
			continue

if __name__ == '__main__':
	#sort_data()
	if not os.path.exists('result.csv'):
		csv_pack('result',['Сайт',"Кол-во ссылок","Кол-во дат","Если слово news в тексте","Последний указаный год"],'w')
	check_if_news()
