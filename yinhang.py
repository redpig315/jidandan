#--utf-8--
#获取银行招聘信息汇总
import requests
from lxml import etree
#from bs4 import BeautifulSoup

headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML,like Gecko) Chrome/53.0.2785.143 Safari/537.36"}

def get_links(url):
	raw_content=requests.get(url,headers=headers)
	#print(raw_content.text)---测试网页
	'''
	soup=BeautifulSoup(raw_content.text,'lxml')
	links=soup.select('#midder > div.ll > div > div:nth-child(4) > dl:nth-child(1) > dt > a')
	for link in links:
		print(link.text)
	'''
	selector=etree.HTML(raw_content.text)
	rows=selector.xpath('//*[@id="midder"]/div[1]/div/div[4]/dl/dt') #rows是个列表
	for row in rows:
		title=row.xpath('a')
		for tmp in title:
			print(tmp.text)

		


#selector is #midder > div.ll > div > div:nth-child(4) > dl:nth-child(1) > dt > a
if __name__ == '__main__':
	url="http://www.yinhangzhaopin.com/new100.htm"
	get_links(url)