#！--utf8--

from bs4 import BeautifulSoup

import requests


headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} 

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL' +'ALL'

try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


fp=open("d:/bookmarks_2022_9_18.html",'r',encoding="utf8")
text=fp.read()
fp.close()
soup=BeautifulSoup(text,'lxml')
#print(soup)

allmarked=soup.find_all('a')

#print(allmarked)

print("raw count:"+str(len(allmarked)))

failed=0


#,verify=False
for mark in allmarked:
	#print(mark.text)
	#print(mark.get('href'))
	try:
		rst=requests.get(mark.get('href'),headers=headers)
		if rst.ok:
			print(mark.get('href'))
		else:
			failed=failed+1
	except requests.exceptions.ConnectionError as e:
		print("++++++++"+str(e)+"++++++++")

print("p count:"+str(len(allmarked)-failed))


#将有效的url重新写回bookmark


   

