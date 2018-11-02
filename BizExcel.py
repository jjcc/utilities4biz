
import xlwings as xw
import os

target = 0 # 0 for bank, 1 for visa

statement_sheets = [0,2]
inflow_tags=["Income","PAYBACK"]

income_tag = inflow_tags[target] #"Income' for bank


bk = xw.books[0]
st = bk.sheets[statement_sheets[target]] # 0 for bank, 2 for visa
rng =st.range('A1:H250')
dic = {}
count = 0
for r in rng.rows:
    (date,content, amountl, amountr,code) = (r[1].value,r[2].value,r[3].value,r[4].value, r[6].value)
    if (date == None):
        continue
    (m,d,y) = date.split('/')
    count +=1
    #print count
    key = m + "-" + y

    if not key in dic:
        dic[key] = {}
    if not code in dic[key]:
        dic[key][code] = 0

    #if ( code == "Income"):
    if (code == income_tag):
        dic[key][code] += amountr
    else:
        if(amountl == None): #refund
            continue
        dic[key][code] += amountl

    #print date, content,amount
    (m,d,y) = date.split('/')
    #print '{0}, {1},{2}'.format(m , content, amountl)
total = 0


for my, v in sorted(dic.items()):
    for code in v:
        if income_tag == code:
            print( "Inflow:\t{}\t\t{}".format(my, v[income_tag]))
            total += v[income_tag]
        else:
            print( "Expense:\t{}\t{}\t{}".format(my, code, v[code]))
    print "\n"


print total