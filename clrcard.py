#使用这个程序用来作为IC卡测试环境洗白的工具，使用须知，需要安装模块ibm_db 
# -----处理流程如下：1.首先检查表cardxxx,如果没有对应卡号，则添加
# -----2.检查表 cardaaa ,有记录则修改acc_sts='*',没有数据则插入一条新记录
# -----3.检查表 cardaa123 ,有记录则修改card_sts='*',没有数据则插入一条新纪录

import ibm_db
import sys
import re


#select 
def querydb(conn,sql):
	stmt=ibm_db.exec_immediate(conn,sql)
	print("exec sql: "+sql)
	result=ibm_db.fetch_both(stmt)
	return result;

#update|insert|delete
def do_sql(conn,sql):
	stmt=ibm_db.exec_immediate(conn,sql)
	print("exec sql: "+sql)
	rows=ibm_db.num_rows(stmt)
	print("%s rows is changed!"%rows)



connstr="DATABASE=xxx;HOSTNAME=xxx;PORT=501100;PROTOCOL=TCPIP;UID=xxx;PWD=xxxxx;"

conn=None;


card_no=sys.argv[1]

if len(card_no)==19:
	regex=re.compile(r'12345\d{13}$')
	cls=regex.search(card_no)
	if not cls:
		sys.exit(0)
	
else:
	sys.exit(0)

try:
	conn=ibm_db.connect(connstr,"","")
	if conn:
		'''#sql="select *from a where 
		#stmt=ibm_db.exec_immediate(conn,sql)
		#result=ibm_db.fetch_both(stmt)
		#if result:
			#print(result)
		#else:
			#print("select is null")'''
		#查询表a
		sql_seqn="select *from a where card_no='%s';"%card_no
		res=querydb(conn,sql_seqn)
		if res:
			print("card is existed!...")
		else:
			insert_sql="insert into a values('%s','01');"%card_no
			do_sql(conn,insert_sql)

		#查询表aa
		sql_acc="select *from aa where card_no='%s';"%card_no
		res=querydb(conn,sql_acc)
		if res:
			update_sql="update aa set acc_sts='*' where card_no='%s';"%card_no
			do_sql(conn,update_sql)
		else:
			insert_sql="insert into aa values('%s','%s' ,'01' '12345678');"%(card_no,card_no)
			do_sql(conn,insert_sql)

		#查询表aa1
		sql_info="select *from aa1 where card_no='%s';"%card_no
		res=querydb(conn,sql_info)
		if res:
			update_sql="update aa1 set card_sts='*' where card_no='%s';"%card_no
			do_sql(conn,update_sql)
		else:
			insert_sql="insert into aa1 values ('0001', '10001', '%s', '01', null);"%card_no
			do_sql(conn,insert_sql)

	else:
		print("conn is err null %s"%conn)
except Exception as e:
	print(e)
finally:
	if conn:
		ibm_db.close(conn)
		print("clear is successed!...")
	else:
	   print("nothing can do!")	

