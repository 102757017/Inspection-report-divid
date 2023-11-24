#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import os
import pprint

def Judge(part_num):
    part_num=part_num[:-1]+"_"
    os.chdir(os.path.dirname(__file__))
    conn = sqlite3.connect(r'D:\hewei\soft\check report2\Partlist.db')

    # 创建一个Cursor:
    cursor = conn.cursor()
    #where后面的多个条件用AND和OR连接运算，where前面的字段用逗号连接
    cursor.execute("select model from table1 where [ts num] like '{}'".format(part_num))
    #同一个cursor执行代码，后一个会覆盖前一个

    '''cursor只能用一次，即每用完一次之后记录其位置，
    等到下次再取的时候是从游标处再取而不是从头再来，
    fetch完所有的数据之后，这个cursor将不再有使用价值了，即不再能fetch到数据了。
    '''
    values = cursor.fetchall()
    pprint.pprint(values)
    # Cursor使用完成后应该尽快关闭，释放内存:
    cursor.close()

    # 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
    conn.commit()
    # 关闭数据库
    conn.close()
    models=[]
    for x in values:
        for y in x:
            models.append(y)
    if len(models)==0:
        models.append("unknow")
    print(models)
    return models

if __name__=="__main__":
    Judge("81660-TBT9-H010-M1-0000")
