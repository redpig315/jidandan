import os

path="."

files=os.listdir(path)
#循环扫描当前目录空文件家
for file in files:
	print("look at ->"+file)
	if os.path.isdir(file):
		if not os.listdir(file):#文件夹为空
			os.rmdir(file)
	elif os.path.isfile(file):
		if os.path.getsize(file)==0:#文件大小为空
			os.remove(file)
print(path+"is scaning over!!")