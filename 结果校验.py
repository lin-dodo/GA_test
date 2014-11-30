import math
import time, MySQLdb    
import datetime
from pylab import*
from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Selectors
from pyevolve import Initializators, Mutators
import pyevolve

list_dic={'IF':[],'CU':[],'I':[],'M':[],'RU':[],'SR':[],'RB':[],'TA':[],'Y':[]}
list_margin={'IF':100000,'CU':30000,'RU':23000,'I':3500,'M':2100,'RB':2500,'SR':4500,'TA':3600,'Y':5400}
list_zhonglei=[]
conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="chaodata",charset="utf8")  
cursor = conn.cursor()
sql="select pinPrefix,leverRatio from pro_information ;"
nn=cursor.execute(sql)
row_dic=cursor.fetchall()
dic_ratio=dict(row_dic)

sql="select pinPrefix,contractUnit from pro_information ;"
nn=cursor.execute(sql)
row_dic=cursor.fetchall()
dic_unit=dict(row_dic)
 
x_len=22
for i in xrange(x_len):
    sql="select * from data where ID=%s ;"%i
    m=cursor.execute(sql)
    row=cursor.fetchone()
    list_zhonglei.append(row[0])
    list_dic[row[0].upper()].append(i)
print 'ok'

def mystd(a):
    l=len(a)
    m=sum(a)/float(l)
    d=0
    for i in a: d+=(i-m)**2
    return math.sqrt(d/l)
def output_test(list_lots):
    global start
    global mid
    s=start.strftime('%y-%m-%d')
    m=mid.strftime('%y-%m-%d')
    mm=m
    all_row_test=[]
    #print s,m,list_lots[0:]
    for i in xrange(len(list_lots)):
        if list_lots[i]>0:
            sql="select * from data where ID=%s and Date>='%s' and Date<'%s';"%(i,s,mm)
            #print s,mm
            m=cursor.execute(sql)
            row=cursor.fetchall()
            all_row_test=all_row_test+list(row)
    return all_row_test
def output_run(list_lots):
    global mid
    global end
    m=mid.strftime('%y-%m-%d')
    e=end.strftime('%y-%m-%d')
    mm=m
    ee=e
    all_row_run=[]
    for i in xrange(len(list_lots)):
        if list_lots[i]>0:
            sql="select * from data where ID=%s and Date>='%s' and Date<'%s' ;"%(i,mm,ee)
            m=cursor.execute(sql)
            row=cursor.fetchall()
            all_row_run=all_row_run+list(row)
    return all_row_run
c=0
def test(list_signal,l):

    global c
    global dic_ratio
    global dic_unit
    total_money=10000000
    total_cost=0
    #buy_lot=0
    #sell_lot=0
    #buy_price=0
    #sell_price=0
    buy_lot=[0]*len(l)
    sell_lot=[0]*len(l)
    buy_price=[0]*len(l)
    sell_price=[0]*len(l)

    profit_rate=[]
    profit=[]
    totalprofit=[]
    for i in list_signal:
        print i
        if c==1:
            print sell_lot
            print sell_price
        symbol=i[0].upper()
        ID=int(i[-1])
        if buy_lot[ID]==0 and i[2]==-2:
            continue
        if sell_lot[ID]==0 and i[2]==2:
            continue
        lot=l[ID]
        if i[2]==1:
            buy_lot[ID]=buy_lot[ID]+lot
            total_money=total_money-i[5]*lot
            buy_price[ID]=(buy_price[ID]*(buy_lot[ID]-lot)+i[3]*lot)/buy_lot[ID]
            
            
        if i[2]==-1:
            sell_lot[ID]=sell_lot[ID]+lot
            total_money=total_money-i[5]*lot
            sell_price[ID]=(sell_price[ID]*(sell_lot[ID]-lot)+i[3]*lot)/sell_lot[ID]
            
        if i[2]==-2:
            buy_lot[ID]=buy_lot[ID]-lot
            total_money=total_money+i[5]*lot
            pro=((i[3]-buy_price[ID])*dic_unit[symbol]-i[-2]*2)*lot
            profit_rate.append(pro/(buy_price[ID]*dic_unit[symbol]*lot))
            profit.append(pro)
            total_money=total_money+profit[-1]
            #print profit[-1]
            totalprofit.append(sum(profit))
            if buy_lot[ID]==0:
                buy_price[ID]=0
        if i[2]==2:
            sell_lot[ID]=sell_lot[ID]-lot
            total_money=total_money+i[5]*lot
            pro=((sell_price[ID]-i[3])*dic_unit[symbol]-i[-2]*2)*lot
            profit_rate.append(pro/(sell_price[ID]*dic_unit[symbol]*lot))
            profit.append(pro)
            total_money=total_money+profit[-1]
            totalprofit.append(sum(profit))
            if sell_lot[ID]==0:
                sell_price[ID]=0
        if total_money<0:
            return 0
##    if sell_lot!=0 or buy_lot!=0:
##        print "wrong"
    #print totalprofit[-1]
    if len(profit)==0:
        return 0
    x=range(0,len(totalprofit))
    plot(x,totalprofit)
    show()
    s=sum(profit_rate)/(mystd(profit_rate)*math.sqrt(len(profit_rate)))
    if s<0:
        s=0
    return s
def run(list_signal,l):
    global dic_ratio
    global dic_unit
    total_money=10000000
    total_cost=0
    #buy_lot=0
    #sell_lot=0
    #buy_price=0
    #sell_price=0
    buy_lot=[0]*len(l)
    sell_lot=[0]*len(l)
    buy_price=[0]*len(l)
    sell_price=[0]*len(l)
    profit_rate=[]
    profit=[]
    totalprofit=[]
    for i in list_signal:
        symbol=i[0].upper()
        ID=int(i[-1])
        if buy_lot[ID]==0 and i[2]==-2:
            continue
        if sell_lot[ID]==0 and i[2]==2:
            continue
        lot=l[ID]
        if i[2]==1:
            buy_lot[ID]=buy_lot[ID]+lot
            total_money=total_money-i[5]*lot
            buy_price[ID]=(buy_price[ID]*(buy_lot[ID]-lot)+i[3]*lot)/buy_lot[ID]
            
            
        if i[2]==-1:
            sell_lot[ID]=sell_lot[ID]+lot
            total_money=total_money-i[5]*lot
            sell_price[ID]=(sell_price[ID]*(sell_lot[ID]-lot)+i[3]*lot)/sell_lot[ID]
            
        if i[2]==-2:
            buy_lot[ID]=buy_lot[ID]-lot
            total_money=total_money+i[5]*lot
            pro=((i[3]-buy_price[ID])*dic_unit[symbol]-i[-2]*2)*lot
            profit_rate.append(pro/(buy_price[ID]*dic_unit[symbol]*lot))
            profit.append(pro)
            total_money=total_money+profit[-1]
            #print profit[-1]
            totalprofit.append(sum(profit))
            if buy_lot[ID]==0:
                buy_price[ID]=0
        if i[2]==2:
            sell_lot[ID]=sell_lot[ID]-lot
            total_money=total_money+i[5]*lot
            pro=((sell_price[ID]-i[3])*dic_unit[symbol]-i[-2]*2)*lot
            profit_rate.append(pro/(sell_price[ID]*dic_unit[symbol]*lot))
            profit.append(pro)
            total_money=total_money+profit[-1]
            totalprofit.append(sum(profit))
            if sell_lot[ID]==0:
                sell_price[ID]=0
        if total_money<0:
            return []
    print "########right"
    return profit

def main_test(l):
    all_row=output_test(l)
    if len(all_row)==0:
        return 0
    all_row.sort(key=lambda x:x[1])
    a=test(all_row,l)
    return a
def main_run(l):
    all_row=output_run(l)
    if len(all_row)==0:
        return []
    all_row.sort(key=lambda x:x[1])
    a=run(all_row,l)
    return a

test_days=30
run_days=30
t1=datetime.timedelta(days=test_days)
t2=datetime.timedelta(days=run_days)
start=datetime.datetime(2010,7,26,0,0,0)
stop=datetime.datetime(2014,9,26,0,0,0)
mid=start+t1
end=start+t2+t1
row_test=[]
row_run=[]

temp=[]
s=start.strftime('%y-%m-%d')
m=mid.strftime('%y-%m-%d')
e=end.strftime('%y-%m-%d')

print s,m,e
a=[0, 0, 5, 0, 100, 27, 0, 0, 6, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#a=[1]*x_len
print main_test(a)


conn.close()
cursor.close()
