#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import time
import os
import pprint

print(os.path.dirname(os.path.dirname(__file__)))
os.chdir(os.path.dirname(os.path.dirname(__file__)))

# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('Partlist.db')

# 创建一个Cursor:
cursor = conn.cursor()
part_num="23-4729920-2"
cursor.execute("select * from table1 where [wico num] = '{}'".format(part_num))
#cursor.execute("select * from table1 where [wico num] like '{}'".format(part_num))


#UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
#cursor.execute("update table1 set [ts num] = '81201-TLAA-A510-M1-0001' where [wico num]=?",(part_num,))
#cursor.execute("update table1 set [wico num] = '21-3488270K-2' where [wico num] like '{}'".format(part_num))
#cursor.execute("delete from table1 where id = '{}'".format(164))

values = cursor.fetchall()
pprint.pprint(values)
print(len(values))



# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()

# 关闭Cursor:
cursor.close()

# 关闭数据库
conn.close()
