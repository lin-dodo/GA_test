# -*- coding: utf-8 -*-
import copy
import math
import time, MySQLdb    
import datetime
import sys
import multiprocessing
list_dic={'IF':[],'CU':[],'I':[],'M':[],'RU':[],'SR':[],'RB':[],'TA':[],'Y':[]}
list_margin={'IF':100000,'CU':30000,'RU':23000,'I':3500,'M':2100,'RB':2500,'SR':4500,'TA':3600,'Y':5400}
list_change_to={'IF':1,'CU':0.895,'RU':0.872,'I':0.709,'M':0.664,'RB':0.68,'SR':0.731,'TA':0.711,'Y':0.746}
list_zhonglei=[]
mysql_result_list=[]
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
    global mysql_result_list
    all_row_test=[]
    for i in xrange(len(list_lots)):
        if list_lots[i]>0:
            all_row_test=all_row_test+[j for j in mysql_result_list if j[-1]==i]
            #sql="select * from data where ID=%s and Date>='%s' and Date<'%s';"%(i,s,mm)
            #all_row_test=all_row_test+list(row)
    return all_row_test
def xiapu(list_signal,l):

    global dic_ratio
    global dic_unit
    total_money=1000000
    per_cost=[]
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

    if len(profit)==0:
        return -10
    s=(totalprofit[-1]/sum(per_cost))/mystd(profit_rate)
    return s

def test(list_signal,l):

    global num_test
    global num_lost
    num_test=num_test+1
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
##        if total_money<0:
##            num_lost=num_lost+1
##            return 0
        
    if len(profit)==0:
        return 0
    s=(totalprofit[-1]/sum(per_cost))/mystd(profit_rate)
    if s<0:
        num_lost=num_lost+1
        s=0
    #print s
    return s
def main_xiapu(l):
    all_row=output_test(l)
    if len(all_row)==0:
        return -10
    all_row.sort(key=lambda x:x[1])
    a=xiapu(all_row,l)
    return a
def main_test(l):
    #print 8888
##    #global list_xiapu
##    #print l[0:]
##    ####################
##    #以下为修复过程：
##    list_sort_xiapu=sorted(list_xiapu)
##    s=0
##    for j in xrange(x_len):
##        s=l[j]*list_per_margin[j]+s
##    if s>1000000:
##        start_index=0
##        while(1):
##            index=list_xiapu.index(list_sort_xiapu[start_index])
##            if l[index]==0:
##                start_index=start_index+1
##                
##            else:
##                l[index]=l[index]-1
##            s=s-list_per_margin[index]
##            if s<1000000:
##                break
##    #print l[0:]
##    ####################
    all_row=output_test(l)
    if len(all_row)==0:
        return 0
    all_row.sort(key=lambda x:x[1])
    a=test(all_row,l)
    return a
test_days=1000
run_days=1000
t1=datetime.timedelta(days=test_days)
t2=datetime.timedelta(days=run_days)
start=datetime.datetime(2011,3,23,0,0,0)
stop=datetime.datetime(2013,11,7,0,0,0)
mid=start+t1
end=start+t2+t1
row_test=[]
row_run=[]
temp=[]
num_test=0
num_lost=0
s=start.strftime('%y-%m-%d')
m=mid.strftime('%y-%m-%d')
e=end.strftime('%y-%m-%d')
sql="select * from data where Date>='%s' and Date<'%s';"%(s,m)
#print s,mm
num=cursor.execute(sql)
row=cursor.fetchall()
mysql_result_list=list(row)
print end
#print main_test([1])
list_xiapu=[0]*x_len
for i in xrange(x_len):
    a=[0]*x_len
    a[i]=1
    #print a
    list_xiapu[i]=main_xiapu(a)

for j in xrange(x_len):
    list_xiapu[j]=list_xiapu[j]/(list_change_to[list_zhonglei[j]])
print list_xiapu
pool = multiprocessing.Pool(processes=4)
##ppservers=()
##if len(sys.argv)>1:
##    ncpus=int(sys.argv[1])
##    job_server=pp.Server(ncpus,ppservers=ppservers,secret="")
##else:
##    job_server=pp.Server(ppservers=ppservers,secret="")
aa=[]
results=[]
t1=time.time()
for i in range(40):
    results.append(pool.apply_async(main_test,([1]*10,)))
#print aa

#results=pool.apply_async(main_test,(aa,))
for i in results:
    print i.get()
pool.close()
pool.join()
t2=time.time()
for i in range(40):
    main_test([1]*10)
t3=time.time()
print t2-t1,t3-t2


#job1=job_server.submit(main_test,(i,),(output_test,mystd),(),globals={main_test:start})
#print main_test([0,0,0,0,1])
#print job1()
