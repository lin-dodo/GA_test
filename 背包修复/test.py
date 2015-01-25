# -*- coding: utf-8 -*-
import copy
import math
import time, MySQLdb  
import datetime
from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Selectors
from pyevolve import Initializators, Mutators
import pyevolve
import multiprocessing
f=open('1-1-背包修复.txt','w+')
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
##    del list_signal
##    del buy_lot,sell_lot
##    gc.collect()
    return s
def run(list_signal,l):
    global dic_ratio
    global dic_unit
    total_money=1200000
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
def main_xiapu(l):
    all_row=output_test(l)
    if len(all_row)==0:
        return -10
    all_row.sort(key=lambda x:x[1])
    a=xiapu(all_row,l)
    return a
def main_test(l):

    #global list_xiapu

##    list_xiapu=[0]*x_len
##    for i in xrange(x_len):
##        a=[0]*x_len
##        a[i]=1
##        #print a
##        list_xiapu[i]=main_xiapu(a)
##    
##    for j in xrange(x_len):
##        list_xiapu[j]=list_xiapu[j]/(list_change_to[list_zhonglei[j]])
    list_xiapu_temp=copy.deepcopy(list_xiapu)
    #print list_xiapu
    ####################
    #以下为修复过程：
    list_sort_xiapu=sorted(list_xiapu_temp)
    s=0
    for j in xrange(x_len):
        s=l[j]*list_per_margin[j]+s
    if s>1000000:
        start_index=0
        while(1):
            index=list_xiapu_temp.index(list_sort_xiapu[start_index])
            if l[index]==0:
                start_index=start_index+1
                
            else:
                l[index]=l[index]-1
            s=s-list_per_margin[index]
            if s<1000000:
                break
    
    #print l[0:]
    ####################
    all_row=output_test(l)
    if len(all_row)==0:
        return 0
    all_row.sort(key=lambda x:x[1])
    a=test(all_row,l)
##    del list_xiapu_temp
##    del list_sort_xiapu
##    del all_row
##    gc.collect()
    return a
def main_run(l):
    all_row=output_run(l)
    if len(all_row)==0:
        return []
    all_row.sort(key=lambda x:x[1])
    a=run(all_row,l)
    return a

test_days=60
run_days=30
t1=datetime.timedelta(days=test_days)
t2=datetime.timedelta(days=run_days)
start=datetime.datetime(2011,3,23,0,0,0)
stop=datetime.datetime(2013,11,7,0,0,0)
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


##def main_main(l):
##    ll=l[0:]
##    a=pool.apply_async(main_test,(ll,))
##    return a.get()
f_per=open('1-1xiufu_per.txt','w+')
while(end<=stop):
    #pool = multiprocessing.Pool(processes=4)
    
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
    f.write(s+' '+m+' '+e+'\n')
    list_xiapu=[0]*x_len
    list_xiapu2=[0]*x_len
    for i in xrange(x_len):
        a=[0]*x_len
        a[i]=1
        #print a
        list_xiapu[i]=main_xiapu(a)
    
    for j in xrange(x_len):
        list_xiapu[j]=list_xiapu[j]/(list_change_to[list_zhonglei[j]])
    print list_xiapu
    print end
    #print main_test([1])
    
    #print list_xiapu
    genome = G1DList.G1DList(x_len)
    genome.setParams(range_list=[10,10,100,100,100,100,100,43,43,43,43,40,40,40,40,40,40,40,40,40,40])
    #genome.setParams(rangemin=0,rangemax=100)
    genome.initializator.set(Initializators.G1DListInitializatorInteger)
    genome.mutator.set(Mutators.G1DListMutatorIntegerGaussian)
    genome.evaluator.set(main_test)
    #genome.crossover.clear()
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setMultiProcessing(flag=True,full_copy=False)
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setMutationRate(0.9)
    ga.setPopulationSize(20)
    ga.setGenerations(40)
    ga.evolve(10)
    best=ga.bestIndividual()
##    pool.close()
##    pool.join()
    #row_test=output_test([1])
    #row_run=output_run([0,1])
##    if len(row_test)>0 and len(row_run)>0:
##        print len(row_test),1
##        print len(row_run),2
    #per=num_lost/float(num_test)
    #f_per.write(str(per))
    #f_per.write('\n')
    print num_lost,num_test
    print best[0:]
    a=best[0:]
    a=str(a)
    f.write(a+'\n')
    temp=temp+main_run(best[0:])
    start=start+t2
    mid=mid+t2
    end=end+t2
print len(temp)
proo=[]
for i in xrange(len(temp)):
    proo.append(sum(temp[:i+1]))
x=xrange(len(proo))
f_per.close()
f.close()
from pylab import*
plot(x,proo)
savefig(r'1-1-背包修复.png')
conn.close()
cursor.close()
