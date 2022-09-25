# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import base64
from urllib.parse import urlparse
import os
import time


headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'} 


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL' +'ALL'

try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


url="https://asmrfun.com/index.php/category/pics/"

def saveimage(url):
#加一点异常处理
	try:
		image=requests.get(url)
		path=urlparse(url).path
		filenames=re.split('/',path)
		if os.path.exists("D:/code/xxoo") == False:
			os.mkdir("D:/code/xxoo")
		f = open("D:/code/xxoo/"+filenames[5]+filenames[6], 'wb')
		f.write(image.content)
		f.flush()
		f.close()
	except requests.exceptions.ConnectionError as e:
		pass



def get_urls(url):
	html = requests.get(url, headers=headers).text
	#print(html)
	soup=BeautifulSoup(html,'html.parser')
	xxoos=soup.find_all('div',{'class':'item-title'})
	for xxoo in xxoos:
		print(xxoo.a.get('href'))
		get_page(xxoo.a.get('href'))
		time.sleep(2)


def get_page(url):
	html = requests.get(url, headers=headers).text
	soup=BeautifulSoup(html,'html.parser')
	images=soup.find('div',{'class':'nbodys'}).find_all('img')
	for image in images:
		#来一点打印，要不以为程序司机了
		print(image)
		saveimage(image.get('src'))



#get_urls(url)

for i in range(2,15):
	print("+++++"+str(i)+"+++++")
	get_urls(url+str(i))
