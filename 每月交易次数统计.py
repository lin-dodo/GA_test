import time, MySQLdb    
import datetime
conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="chaodata",charset="utf8")  
cursor = conn.cursor()
f=open('统计结果.csv','w+')
f.write('时间')

for i in range(0,21):
    sql="select * from `index` where ID=%s ;"%i
    #print sql
    m=cursor.execute(sql)
    row=cursor.fetchall()
    row=list(row)
    f.write(','+row[0][0][:-16])
f.write('\n')
def output_test():
    global start
    global end
    s=start.strftime('%y-%m-%d')
    e=end.strftime('%y-%m-%d')
    f.write(s+'to'+e)
    ee=e
    all_row=[0]*21
    for i in xrange(21):
            sql="select * from data where ID=%s and Date>='%s' and Date<'%s';"%(i,s,ee)
            m=cursor.execute(sql)
            f.write(','+str(m))
    f.write('\n')

t1=datetime.timedelta(days=30)
start=datetime.datetime(2010,7,26,0,0,0)
stop=datetime.datetime(2014,10,8,0,0,0)
end=start+t1
while(end<=stop):
    s=start.strftime('%y-%m-%d')
    e=end.strftime('%y-%m-%d')
    print s,e
    output_test()
    start=start+t1
    end=end+t1
f.close()
conn.close()
cursor.close()
