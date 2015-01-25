# -*- coding: utf-8 -*-
import copy
import math
import time, MySQLdb    
import datetime
from pylab import*
list_dic={'IF':[],'CU':[],'I':[],'M':[],'RU':[],'SR':[],'RB':[],'TA':[],'Y':[]}
list_margin={'IF':100000,'CU':30000,'RU':23000,'I':3500,'M':2100,'RB':2500,'SR':4500,'TA':3600,'Y':5400}
list_change_to={'IF':1,'CU':0.895,'RU':0.872,'I':0.709,'M':0.664,'RB':0.68,'SR':0.731,'TA':0.711,'Y':0.746}
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
 
x_len=21
for i in xrange(x_len):
    sql="select * from data where ID=%s ;"%i
    m=cursor.execute(sql)
    row=cursor.fetchone()
    list_zhonglei.append(row[0])
    list_dic[row[0].upper()].append(i)
print 'ok'
list_per_margin=[0]*x_len
for i in xrange(x_len):
    list_per_margin[i]=list_margin[list_zhonglei[i]]

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
def test(list_signal,l):
    global dic_ratio
    global dic_unit
    total_money=1200000
    per_cost=[]
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
            per_cost.append((buy_price[ID]*dic_unit[symbol]*dic_ratio[symbol]+i[-2]*2)*lot)
            profit_rate.append(pro/per_cost[-1])
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
            per_cost.append((sell_price[ID]*dic_unit[symbol]*dic_ratio[symbol]+i[-2]*2)*lot)
            profit_rate.append(pro/per_cost[-1])
            profit.append(pro)
            total_money=total_money+profit[-1]
            totalprofit.append(sum(profit))
            if sell_lot[ID]==0:
                sell_price[ID]=0
    x=xrange(len(totalprofit))

    plot(x,totalprofit)
    show()
    print totalprofit[-1]
    if len(profit)==0:
        return 0
    print totalprofit[-1],sum(per_cost),mystd(profit_rate)
    s=(totalprofit[-1]/sum(per_cost))/mystd(profit_rate)
    if s<0:
        s=0
    return s
def main_test(l):
    all_row=output_test(l)
    if len(all_row)==0:
        return 0
    all_row.sort(key=lambda x:x[1])
    a=test(all_row,l)
    return a
test_days=60
run_days=30
t1=datetime.timedelta(days=test_days)
t2=datetime.timedelta(days=run_days)
start=datetime.datetime(2011,3,23,0,0,0)
stop=datetime.datetime(2013,12,7,0,0,0)
mid=start+t1
end=start+t2+t1
print main_test([0,0,0,0,0,0,0,1])
row_test=[]
row_run=[]
temp=[]
