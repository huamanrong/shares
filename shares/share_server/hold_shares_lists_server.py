from queue import Queue
from shares.share_server import database
from shares.share_until.creat_thread import create_thread
from shares.share_until.shares_real_time_prices import Stock
from shares.share_until.mysql_until import *


class HoldSharesListsServer:
    def __init__(self, shares_user, logger):
        self.shares_user = shares_user
        self.logger = logger
        self.work_queue = Queue()

    def get_items_value(self):
        sql = '''
        SELECT
            all_shares.ts_code,
            all_shares.`name`,
            buy_already.cost,
            buy_already.amount,
            shares_user.surplus_money
        FROM
            all_shares,
            buy_already,
            shares_user
        WHERE
            buy_already.`status` = 1
            AND buy_already.user_id=%s
            AND buy_already.symbol=all_shares.symbol
            AND shares_user.id = buy_already.user_id
            ORDER BY buy_already.buy_datetime
        '''
        conf = database.conf
        result = execute_select_sql(conf, sql, self.logger, self.shares_user)
        # print(result)   # (('sh600884', '杉杉股份', 14.0, 500, 41000.0), ('sz000008', '神州高铁', 2.0, 1000, 41000.0))
        if result:
            join_list = [ts_code[0] for ts_code in result]
            join_ts_code = ','.join(join_list)
            share = Stock(join_ts_code)
            share.run()
            # while True:
            queue_value = share.work_queue.get()  # {'杉杉股份': '14.870,15.540', '神州高铁': '2.180,2.170'}
            print(queue_value)
            share.work_queue.task_done()
            if queue_value:
                new_result = []
                hold_shares_amount = 0  # 股票总市值，计算仓位用的，仓位计算：当前股票总市值/(所有股票总市值+流动资金)
                for shares_msg in result:
                    sub_list = []
                    price_list = queue_value[shares_msg[1]].split(',')
                    price_list = [float(price) for price in price_list]
                    total_profit = round(price_list[0] * shares_msg[3] - shares_msg[2] * shares_msg[3], 2)
                    today_profit = round((price_list[0] - price_list[1]) * shares_msg[3], 2)
                    hold_shares_amount += price_list[0] * shares_msg[3]
                    sub_list.append(shares_msg[1])
                    sub_list.append(total_profit)
                    sub_list.append('%s/%s' % (shares_msg[2], price_list[0]))
                    sub_list.append(shares_msg[3])
                    sub_list.append(today_profit)
                    new_result.append(sub_list)
                for index, sub_msg in enumerate(new_result):
                    shares_amount = float(sub_msg[2].split('/')[1]) * sub_msg[3]
                    total_amount = hold_shares_amount + result[0][4]
                    position = '{:.1%}'.format(round(shares_amount / total_amount, 3))
                    new_result[index].append(position)
                # print(new_result)
                self.work_queue.put(new_result)
        else:
            self.work_queue.put([])
