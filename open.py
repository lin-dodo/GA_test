
# -*- coding:utf8 -*-
import os
import csv
import time, MySQLdb 
conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="chaodata",charset="utf8")  
cursor = conn.cursor()

def write(path,n):
    with open(path,'rb')as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)==8:
                sql="insert into `data`(`Symbol`,`Date`,`Signal`,`Price`,`Status`,`Margin`,`Poundage`,`ID`)values('%s','%s','%s','%s','%s','%s','%s','%s')"%(row[0],row[1]+" "+row[2],row[3],row[4],row[5],row[6],row[7],n)
            if len(row)==7:
                sql="insert into `data`(`Symbol`,`Date`,`Signal`,`Price`,`Status`,`Margin`,`Poundage`,`ID`)values('%s','%s','%s','%s','%s','%s','%s','%s')"%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],n)
            cursor.execute(sql)
def printPath(path):

    '''
    打印一个目录下的所有文件夹和文件
    '''
    # 所有文件夹，第一个字段是次目录的级别
    filename=[]
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)

    for f in files:
        if(os.path.isdir(path + '//' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if(f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if(os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(path + '/' + f)
            filename.append(f)
    return filename,fileList
filename,fileList=printPath('C:/data_write')
print "总文件数 =", len(fileList)
j=0
for i in filename:
    sql="insert into `index`(`Name`,`ID`)values('%s','%s')"%(i[:-4],j)
    m=cursor.execute(sql)
    write(fileList[j],j)
    print j
    j=j+1

cursor.close()
conn.commit()
conn.close()
