#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import os
import pprint

#识别WICO零件号
def Judge_W(part_num):
    #part_num=part_num[:-1]+"_"
    os.chdir(os.path.dirname(__file__))
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('Partlist.db')

    # 创建一个Cursor:
    cursor = conn.cursor()
    #where后面的多个条件用AND和OR连接运算，where前面的字段用逗号连接
    cursor.execute("select model from table1 where [wico num] = '{}'".format(part_num))
    #同一个cursor执行代码，后一个会覆盖前一个

    '''cursor只能用一次，即每用完一次之后记录其位置，
    等到下次再取的时候是从游标处再取而不是从头再来，
    fetch完所有的数据之后，这个cursor将不再有使用价值了，即不再能fetch到数据了。
    '''
    values = cursor.fetchall()
    #pprint.pprint(values)
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
    
    return models

#识别TS-GSK零件号
def Judge_T(part_num):
    part_num=part_num[:-1]+"_"
    os.chdir(os.path.dirname(__file__))
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('Partlist.db')

    # 创建一个Cursor:
    cursor = conn.cursor()
    #where后面的多个条件用AND和OR连接运算，where前面的字段用逗号连接
    cursor.execute("select table1.model from table1 where table1.'ts num'like ?",(part_num,))
    #同一个cursor执行代码，后一个会覆盖前一个

    '''cursor只能用一次，即每用完一次之后记录其位置，
    等到下次再取的时候是从游标处再取而不是从头再来，
    fetch完所有的数据之后，这个cursor将不再有使用价值了，即不再能fetch到数据了。
    '''
    values = cursor.fetchall()
    #pprint.pprint(values)
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
    models=Judge_W("2311-419-520")
    #models=Judge_T("81670-TLA7-C010-M1-0002")
    print(models)
