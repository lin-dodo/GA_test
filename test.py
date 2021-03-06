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
 
x_len=30
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
    all_row=[]
    #print s,m,list_lots[0:]
    for i in xrange(len(list_lots)):
        if list_lots[i]>0:
            sql="select * from data where ID=%s and Date>='%s' and Date<'%s';"%(i,s,mm)
            #print s,mm
            m=cursor.execute(sql)
            row=cursor.fetchall()
            row=list(row)
            if len(row)>0:
                if row[0][2]==2 or row[0][2]==-2:
                    del row[0]
                all_row=all_row+row
    return all_row
def output_run(list_lots):
    global mid
    global end
    m=mid.strftime('%y-%m-%d')
    e=end.strftime('%y-%m-%d')
    mm=m
    ee=e
    all_row=[]
    for i in xrange(len(list_lots)):
        if list_lots[i]>0:
            sql="select * from data where ID=%s and Date>='%s' and Date<'%s' ;"%(i,mm,ee)
            m=cursor.execute(sql)
            row=cursor.fetchall()
            row=list(row)
            if len(row)>0:
                if row[0][2]==2 or row[0][2]==-2:
                    del row[0]
                all_row=all_row+row
    return all_row
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
    buy_lot={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    sell_lot={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    buy_price={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    sell_price={'IF':0,'CU':0,'I':0,'M':0,'RU':0,'SR':0,'RB':0,'TA':0,'Y':0}
    profit_rate=[]
    profit=[]
    totalprofit=[]
    for i in list_signal:
        if c==1:
            print sell_lot
            print sell_price
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
    #print totalprofit[-1]
    if len(profit)==0:
        return 0
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

test_days=100
run_days=100
t1=datetime.timedelta(days=test_days)
t2=datetime.timedelta(days=run_days)
start=datetime.datetime(2010,7,26,0,0,0)
stop=datetime.datetime(2012,7,26,0,0,0)
mid=start+t1
end=start+t2+t1
row_test=[]
row_run=[]

##genome = G1DList.G1DList(x_len)
###genome.setParams(rangemin=0,rangemax=2)
##genome.My_set(list_dic,list_margin,1000000,list_zhonglei)
##genome.initializator.set(Initializators.G1DListInitializatorInteger_my)#G1DListInitializatorInteger_my)
##genome.mutator.set(Mutators.G1DListMutatorInteger_my)
##genome.evaluator.set(main_test)
##genome.crossover.clear()
##ga = GSimpleGA.GSimpleGA(genome)
##ga.selector.set(Selectors.GRouletteWheel)
##ga.setMutationRate(0.8)
##ga.setPopulationSize(20)
##ga.setGenerations(20)
temp=[]
while(end<=stop):
    print end
    genome = G1DList.G1DList(x_len)
    #genome.setParams(rangemin=0,rangemax=2)
    genome.My_set(list_dic,list_margin,1000000,list_zhonglei)
    genome.initializator.set(Initializators.G1DListInitializatorInteger_my)#G1DListInitializatorInteger_my)
    genome.mutator.set(Mutators.G1DListMutatorInteger_my)
    genome.evaluator.set(main_test)
    genome.crossover.clear()
    ga = GSimpleGA.GSimpleGA(genome)
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setMutationRate(0.8)
    ga.setPopulationSize(50)
    ga.setGenerations(50)
    ga.evolve(50)
    best=ga.bestIndividual()

    print best[0:]
    temp=temp+main_run(best[0:])
    start=start+t2
    mid=mid+t2
    end=end+t2
print len(temp)
proo=[]
for i in xrange(len(temp)):
    proo.append(sum(temp[:i+1]))
x=xrange(len(proo))
plot(x,proo)
show()
    
conn.close()
cursor.close()
