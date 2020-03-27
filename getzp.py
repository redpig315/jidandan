#--utf-8--
#获取银行招聘信息汇总
import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import sqlite3
import datetime
import time
import matplotlib.pyplot as plt

headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML,like Gecko) Chrome/53.0.2785.143 Safari/537.36"}

#从网络获取内容
def get_links(url):
	raw_content=requests.get(url,headers=headers)
	html=raw_content.text
	return html


#从本地文件获取内容
def  get_local(url):
	fp=open(url,'r')
	raw_text=fp.read()
	fp.close()
	return raw_text

###midder > div.ll > div > div:nth-child(4) > dl:nth-child(1) > dd:nth-child(3)
def get_zpinfo(raw_text,filename,database):
	bs=BeautifulSoup(raw_text,"lxml")
	cnt=0
	fullcontent=""
	#获取当前日期
	curdate=str(datetime.date.today())
	#删除当日查询记录，以便导入
	delcur(database,curdate)
	#延迟几秒方便看结果
	time.sleep(5)
	contents=bs.select("#midder > div.ll > div > div:nth-child(4) > dl")
	for zplist in contents:
		title=zplist.find('a').get_text() #标题
		raw_date=zplist.select("dd.list")[0].text  #发布日期
		date=re.search(r'\d\d\d\d-\d\d-\d\d',raw_date).group()
		location=zplist.select("dd")[1]  #工作地点
		url=zplist.find('a').get("href") #连接
		print(title+"   "+date+"  "+location.text+" "+url)
		if(date==curdate): 
			insertdb(database,title,location.text,date,url) 
			cnt=cnt+1
		fullcontent=fullcontent+title+","+date+","+location.text+","+url+"\n"    
		print("++++++++++++++++")
	print("========database insert $"+str(cnt)+"条")
	save2file(filename,fullcontent)#把信息存入txt
	get_data(database)

#保存信息到文件
def save2file(filename,content):
	fp=open(filename,'w')
	fp.write(content)
	fp.close()		


#创建数据库
def createdb(database):
	conn=sqlite3.connect(database)
	c=conn.cursor()
	crtsql='''
	create table zpinfo(
    titile text,
    location char(50),
    fbdate  char(20),
    url   text,
    summary text
	);
	'''
	c.execute(crtsql)
	conn.commit()
	conn.close()

#简单的插入数据库
def insertdb(database,title,location,fbdate,url):
	conn=sqlite3.connect(database)
	c=conn.cursor()
	#print("open database:"+database+"sucess!")
	sql="insert into zpinfo values (  '"+title+"', '"+location+"','"+fbdate+"','"+url+"','');"
	c.execute(sql)
	conn.commit()
	conn.close()

#爬行去重 去除国内外时事政治，数据库插入如何检索最新的记录进行插入，根据日期进行检索

#删除当天记录，以便重复导入，去重
def  delcur(database,date):
	conn=sqlite3.connect(database)
	c=conn.cursor()
	sql="delete from zpinfo where fbdate='"+date+"';"
	c.execute(sql)
	conn.commit()
	print("删除总条数 :",conn.total_changes)


#画图并保存，只显示前30条数据
def get_data(database):
	x=[]
	y=[]
	cnt=0
	conn=sqlite3.connect(database)
	c=conn.cursor()
	sql="select location ,count(location) as a from zpinfo where location <>'' group by location  order by a desc"
	rows=c.execute(sql)
	for row in rows:
		y.append(row[1])
		x.append(row[0])
		cnt=cnt+1
		if cnt>30:
			break
	conn.close()
	show_map(x,y)





#统计一下信息地点，展示图片
def show_map(x,y):
	plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文
	#plt.xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi],['0',r'$\frac{\pi}{2}$',r'$\pi$',r'$\frac{3\pi}{2}$',r'$2\pi$'], rotation=90)# 第一个参数是值，第二个参数是对应的显示效果(若无传入则默认直接显示原始数据)，第三个参数是标签旋转角度
	plt.figure(figsize = (10,20)) 
	plt.bar(x,y, label="招聘信息")
	plt.xticks(rotation=-90)#标签倒置 
	plt.xticks(fontsize = 8)#缩小字体方便查看
	plt.legend()
	plt.xlabel('城市')
	plt.ylabel('招聘数量')
	plt.title('银行招聘信息统计')
	plt.show()



#selector is #midder > div.ll > div > div:nth-child(4) > dl:nth-child(1) > dt > a
if __name__ == '__main__':
	url="http://www.yinhangzhaopin.com/new100.htm"
	html=get_links(url)
	ldir="D:/coding/new100.html"
	database="D:/coding/zhaopin.db"
	zhaopinfile="d:/coding/yinhangzhaopin.txt"
	#html=get_local(ldir)
	#createdb(database)
	get_zpinfo(html,zhaopinfile,database)

