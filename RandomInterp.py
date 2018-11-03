import random
from random import *

import datetime
from dateutil import rrule
'''
randomly generate some number
'''

base = 16

def f(n,s):
    r=min(s,1)
    x=uniform(max(0,r-(r-s/n)*2),r)
    if (n<2) :
        return [s]
    else:
        return  sample([x]+f(n-1,s-x),n)
    #return n<2 and[s]or sample([x]+f(n-1,s-x),n)


def generateseg (startp, len, startv, targetsum):
    '''
    generate a segment
    '''
    abnorm_no =  int( len/5)
    abnorm_idx = f(abnorm_no,len)


    tempmlg = []
    for i in range(1,len):
        r = random() * 8 + base
        #sum += r
        tempmlg.append(r)
        pass

    sumtemp = sum(tempmlg)
    delta = targetsum - sumtemp
    avg = int(delta/len)
    for i in abnorm_idx:
        tempmlg [i] +=avg
    
    return tempmlg


def main():
    days = 120
    daily = []

    start = datetime.datetime(2018, 4, 1)
    end = datetime.datetime(2018, 9, 30)
    rule = rrule.rrule(dtstart=start, freq=rrule.DAILY,count = days,
        byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR]
    )

    a2 = rule.between(start, end, inc=True)

    a1 = list(rule)
    #print(a1)

    #i would be doe, r would be random salt
    #base = 16
    sum = 0 #96000


    abnormals = 5

    abnormal_index = f(abnormals,days) # among total # days, there are # of abnormals

    known =  { 48:1093, 76:1732,115:1562 }

    # get diff of final sum and target, 
    # generate gaps that can fill in the diff
    # filling the gaps in the abnormal index of day.
    sum = 0
    segcount = 0
    prepoint = 0
    prevsum = 0
    for midpoint in known: # to 10L:

        gap = midpoint - prepoint
        targetsum = known[midpoint] - prevsum
        midresult = generateseg(midpoint, gap, 10000, targetsum )

        print("%s, %s,gap: %d"%(midpoint , known[midpoint],gap))    
        segcount += 1
        prepoint = midpoint
        prevsum = known[midpoint]

    print("End of main")
    pass
    return

    for i in range(1, days):
        r = random() * 8 + base #sum += r
        daily.append(r)
    #    final_unit = i + r
    #
    #
    #partial_node = [ 1, 4, 7, 14, ]

    #listr = f(10,100)
    #print (listr)

    for i in range(0, days-1):
        datestr = str(a1[i])
        r = daily[i]
        sum += r
        print ("%d:%s, ##, %d, %d "%(i,datestr,r,sum))


if __name__ == "__main__":
    main()

