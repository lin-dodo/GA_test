import math
import time, MySQLdb    
import datetime
from pylab import*  
list_dic={'IF':[],'CU':[],'I':[],'M':[],'RU':[],'SR':[],'RB':[],'TA':[],'Y':[]}
list_margin={'IF':90000,'CU':30000,'RU':10000,'I':3500,'M':1500,'RB':1500,'SR':3000,'TA':2000,'Y':3500}
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
 
x_len=10
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
def output(list_lots):
    all_row=[]
    for i in xrange(len(list_lots)):
        if list_lots[i]>0:
            sql="select * from data where ID=%s ;"%i
            m=cursor.execute(sql)
            row=cursor.fetchall()
            all_row=all_row+list(row)
    return all_row

def exe(list_signal,l):
    global dic_ratio
    global dic_unit
    total_money=10000000
    total_cost=0
    #buy_lot=0
    #sell_lot=0
    #buy_price=0
    #sell_price=0
    buy_lot={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    sell_lot={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    buy_price={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    sell_price={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    profit_rate=[]
    profit=[]
    totalprofit=[]
    for i in list_signal:
        
        symbol=i[0].upper()
        if buy_lot[symbol]==0 and i[2]==-2:
            continue
        if sell_lot[symbol]==0 and i[2]==2:
            continue
        lot=l[i[-1]]
        if i[2]==1:
            buy_lot[symbol]=buy_lot[symbol]+lot
            total_money=total_money-i[5]*lot
            buy_price[symbol]=(buy_price[symbol]*(buy_lot[symbol]-lot)+i[3]*lot)/buy_lot[symbol]
            
            
        if i[2]==-1:
            sell_lot[symbol]=sell_lot[symbol]+lot
            total_money=total_money-i[5]*lot
            sell_price[symbol]=(sell_price[symbol]*(sell_lot[symbol]-lot)+i[3]*lot)/sell_lot[symbol]
            
        if i[2]==-2:
            buy_lot[symbol]=buy_lot[symbol]-lot
            total_money=total_money+i[5]*lot
            pro=((i[3]-buy_price[symbol])*dic_unit[symbol]-i[-2]*2)*lot
            profit_rate.append(pro/(buy_price[symbol]*dic_unit[symbol]*lot))
            profit.append(pro)
            total_money=total_money+profit[-1]
            #print profit[-1]
            totalprofit.append(sum(profit))
            if buy_lot[symbol]==0:
                buy_price[symbol]=0
        if i[2]==2:
            sell_lot[symbol]=sell_lot[symbol]-lot
            total_money=total_money+i[5]*lot
            pro=((sell_price[symbol]-i[3])*dic_unit[symbol]-i[-2]*2)*lot
            profit_rate.append(pro/(sell_price[symbol]*dic_unit[symbol]*lot))
            profit.append(pro)
            total_money=total_money+profit[-1]
            totalprofit.append(sum(profit))
            if sell_lot[symbol]==0:
                sell_price[symbol]=0
        if total_money<0:
            return 0
##    if sell_lot!=0 or buy_lot!=0:
##        print "wrong"
    x=xrange(len(totalprofit))
    plot(x,totalprofit)
    show()
    print totalprofit[-1]
    return sum(profit_rate)/(mystd(profit_rate)*math.sqrt(len(profit_rate)))
    
    
##    if len(totalprofit)==0:
##        return 0
##    else:
##        return totalprofit[-1]
def main(l):
    #start=time.time()
    i=0
    a=[]
    for j in xrange(len(l)):
        i=i+l[j]
        a.append(l[j])
    if i>333:
        return 0

    all_row=output(l)

    all_row.sort(key=lambda x:x[1])
    #print len(all_row)
    a=exe(all_row,l)
    #end=time.time()
    #print end-start
    return a

print main([47,47,47,1,1,1,1,1])

conn.close()
cursor.close()
