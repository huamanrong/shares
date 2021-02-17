__author__ = 'felix'
# 新浪获取股票行情接口详解：https://blog.csdn.net/simon803/article/details/7784682
import requests
from queue import Queue


class Stock(object):
    def __init__(self, code):
        self.code = code
        self.work_queue = Queue()

    def value_price_get(self):
        slice_num, value_num = 21, 3
        name, now, yesterday = '', '', ''
        if self.code in ['s_sh000001', 's_sz399001']:
            slice_num = 23
            value_num = 1
        response = requests.get("http://hq.sinajs.cn/list=%s" % self.code)
        res_list = response.text.replace('\n', '').split(';')
        res_dict = {}
        for r in res_list:
            res = r.split(',')
            if len(res) > 1:
                name, now, yesterday = res[0][slice_num:], res[value_num], res[2]
            res_dict[name] = '%s,%s' % (now, yesterday)
        self.work_queue.put(res_dict)

    def run(self):
        for i in self.code.split(','):
            if i[:-6] not in ('sh', 'sz', 's_sh', 's_sz'):
                raise ValueError
        # while True:
        #     self.value_price_get()
        #     time.sleep(self.sleep_time)
        self.value_price_get()


if __name__ == '__main__':
    pass
