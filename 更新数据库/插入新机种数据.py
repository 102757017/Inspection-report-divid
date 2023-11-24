# -*- coding: UTF-8 -*-
import os
import sys
import pprint
import sqlite3
import time
import os
import pprint

os.chdir(sys.path[0])
f = open('工作簿1.txt','r') # 读模式

os.chdir(os.path.dirname(os.path.dirname(__file__)))
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('Partlist.db')
# 创建一个Cursor:
cursor = conn.cursor()


while True:
    l=f.readline()
    if l !="":
        #去掉字符串末端的换行符
        l=l.replace('\n','')
        line=l.split("#")
        pprint.pprint(line)
        wico_num=line[0]
        ts_num=line[1]
        part_name=line[2]
        model=line[3]
        cursor.execute("insert into table1 values (?,?,?,?,?)",(None,line[0],line[1],line[2],line[3]))
    else:
        break
    
f.close()


# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()

# 关闭Cursor:
cursor.close()

# 关闭数据库
conn.close()
