import os
#重命名文件名，给文件加上后缀

dirimg=os.listdir('.')
path=os.getcwd()

for file in (dirimg):
	if file!="changegif.py":
		os.rename(os.path.join(path,file),os.path.join(path,file+".gif"))
		print("=====file is "+ os.path.join(path,file+".gif")+"=====")
	