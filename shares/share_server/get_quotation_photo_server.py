import os
import requests
from shares.share_server import database
from shares.share_until.mysql_until import *


class GetQuotationPhotoServer:
    def __init__(self, logger, shares_name):
        self.logger = logger
        self.shares_name = shares_name

    def get_min_quotation_photo(self):  # 当日分时
        sql = 'select ts_code from all_shares where name=%s'
        res = execute_select_sql(database.conf, sql, self.logger, self.shares_name)
        print('http://image.sinajs.cn/newchart/min/n/%s.gif' % res[0][0])
        res = requests.get('http://image.sinajs.cn/newchart/min/n/%s.gif' % res[0][0]).content
        parent_path = os.path.realpath(__file__).replace('\shares\share_server\get_quotation_photo_server.py', '')
        print('parent_path', parent_path)
        with open(os.path.join(parent_path, '%s.jpg' % self.shares_name), 'wb') as f:
            f.write(res)

    def get_daily_quotation_photo(self):    # 日K线
        pass


if __name__ == '__main__':
    GetQuotationPhotoServer('', '晋控煤业').get_min_quotation_photo()