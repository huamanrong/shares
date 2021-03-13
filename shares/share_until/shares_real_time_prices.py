__author__ = 'felix'
# 新浪获取股票行情接口详解：https://blog.csdn.net/simon803/article/details/7784682
import requests
from queue import Queue


class Stock(object):
    def __init__(self, code):
        self.code = code
        self.work_queue = Queue()

    def value_price_get(self):
        name, now, yesterday = '', '', ''
        # print("http://hq.sinajs.cn/list=%s" % self.code)
        response = requests.get("http://hq.sinajs.cn/list=%s" % self.code)
        res_list = response.text.replace('\n', '').split(';')
        res_dict = {}
        code_list = self.code.split(',')
        for index, r in enumerate(res_list):
            res = r.split(',')
            if len(res) > 1:
                if code_list[index] not in ['s_sh000001', 's_sz399001']:
                    slice_num, value_num = 21, 3
                    name, now, yesterday = res[0][slice_num:], res[value_num], res[2]
                else:
                    slice_num, value_num = 23, 1
                    name, now, yesterday = res[0][slice_num:], res[value_num], str(float(res[value_num]) - float((res[2])))
            res_dict[name.replace(' ', '')] = '%s,%s' % (now, yesterday)
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
