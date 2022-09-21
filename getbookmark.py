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

fpmark=open("d:/bookmars_sort.html",'w',encoding="utf8")

fpmark.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")

fpmark.write("<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">\n")

fpmark.write("<TITLE>Bookmarks</TITLE>\n")

fpmark.write("<H1>Bookmarks</H1>\n")

fpmark.write("<DL><p>\n")

fpmark.write("<DT><H3 ADD_DATE=\"1562840722\" LAST_MODIFIED=\"1649945997\" PERSONAL_TOOLBAR_FOLDER=\"true\">书签栏</H3>\n")

fpmark.write("<DL><p>\n")





fp=open("d:/bookmarks_2022_9_21.html",'r',encoding="utf8")
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
			fpmark.write("<DT><A HREF=\""+mark.get('href')+"\">"+mark.text+"</A>\n")
		else:
			failed=failed+1
	except requests.exceptions.ConnectionError as e:
		print("++++++++"+str(e)+"++++++++")

print("p count:"+str(len(allmarked)-failed))



fpmark.write("</DL><p>\n")

fpmark.close()
#将有效的url重新写回bookmark


   

