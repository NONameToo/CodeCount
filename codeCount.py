# coding=utf-8
import os
import time
from  MySQLdb import *


basedir = '/home/python/Desktop'
dir = input("请输入遍历的目录:")
print(dir)

# 如果输入了目录,就拼接目录
if dir:
    walk_dir = os.path.join(basedir, dir)
    print(walk_dir)

else:
    # 如果没有输入任何内容,就默认为当前工作目录
    walk_dir = os.getcwd()
    print(walk_dir)
filelists = []
# 指定想要统计的文件类型
whitelist = ['txt', 'py']
# 遍历文件, 递归遍历文件夹中的所有
def getFile(basedir):

    print("---------------------开始遍历---------------------")
    for parent, dirnames, filenames in os.walk(walk_dir):
        for filename in filenames:
            ext = filename.split('.')[-1]
            #只统计指定的文件类型，略过一些log和cache文件
            if ext in whitelist:
                filelists.append(os.path.join(parent, filename))

# 统计一个文件的行数
def countLine(fname):
    count = 0
    for file_line in open(fname).readlines():
        # 过滤掉空行
        if file_line != '' and file_line != '\n':
            count += 1
    print("%s有: %d行" % (fname, count))
    return count


def save_date(count):
    """把数据存到数据库"""
    conn = connect(host='localhost', port=3306, user='root', passwd='fushaokai', db="MyCodeLife", charset='utf8')
    cursor1 = conn.cursor()
    sql = 'insert into CodeCount(count) values (%s)'
    try:
        print(count)
        cursor1.execute(sql, [count])
    except Exception as e:
        print("出错了,原因是: %s" % e)
    else:
        conn.commit()
        print("============保存记录成功============")

    finally:
        cursor1.close()
        conn.close()

if __name__ == '__main__':
    startTime = time.clock()
    getFile(basedir)
    totalline = 0
    for filelist in filelists:
        totalline = totalline + countLine(filelist)

    print('----------------遍历完成-总共耗时: %0.2f 秒------------' % (time.clock() - startTime))
    print('该目录下文件共计: %d 行' % totalline)
    whether_save = input("是否把记录存入数据库,Yes/No???\n")
    if whether_save in ["y", "yes", "YES", "Yes"]:
        save_date(totalline)


