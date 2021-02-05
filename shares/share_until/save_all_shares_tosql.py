import pymysql
import csv
'插入A股所有股票信息'


conf = {'host': '115.29.185.200',    # 预发
        'user': 'root',
        'password': '351127',
        'port': 3306,
        'database': 'shares',
        'charset': 'utf8'}


def insert_all_shares():
    file = csv.reader(open('shares.csv', 'r'))
    share_list = []
    n = 0
    for i in file:
        if n > 0:
            symbol = '"%s"' % ('0'*(6-len(i[2]))+i[2])
            ts_code = '"%s"' % (i[1][-2:].lower()+i[1][:6])
            name = '"%s"' % i[3]
            area = '"%s"' % i[4]
            industry = '"%s"' % i[5]
            market = '"%s"' % i[6]
            list_status = '"%s"' % i[7]
            list_date = '"%s"' % i[8]
            l = [symbol, ts_code, name, area, industry, market, list_status, list_date]
            new_l = '(%s)' % (','.join(l))
            # print(new_l)
            share_list.append(new_l)
        n += 1
    insert_sql = 'insert into all_shares(symbol,ts_code,`name`,area,industry,market,list_status,list_date)values'
    all_share = ','.join(share_list)
    insert_sql += all_share
    # print(insert_sql)

    cnn = pymysql.connect(**conf)
    cursor = cnn.cursor()
    try:
        cursor.execute(insert_sql)
        cnn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnn.close()