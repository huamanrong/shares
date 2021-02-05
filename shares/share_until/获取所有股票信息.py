'''
https://tushare.pro/document/2
'''

import tushare as ts
import pandas
import datetime
pro = ts.pro_api()

#查询当前所有正常上市交易的股票列表
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_status,list_date')
data.to_csv('shares.csv')
