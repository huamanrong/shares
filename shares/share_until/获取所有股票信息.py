'''
https://tushare.pro/document/2
'''

import tushare as ts
import pandas
import time
import datetime
import requests
# pro = ts.pro_api()

#查询当前所有正常上市交易的股票列表
# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_status,list_date')
# data.to_csv('shares.csv')
t1 = time.time()
res = requests.get('http://image.sinajs.cn/newchart/min/n/sh000001.gif').content
with open('min.gif', 'wb') as f:
    f.write(res)
t2 = time.time()
print(t2-t1)
