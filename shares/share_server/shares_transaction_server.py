import time
from shares.share_until.mysql_until import *
from shares.share_server import database
from shares.share_until.shares_calculation import *


class SharesTransactionServer:
    def __init__(self, logger, shares_user, shares_name, cost, amount, reasons, date_time):
        self.logger = logger
        self.shares_user = shares_user
        self.shares_name = shares_name
        self.cost = cost
        self.amount = amount
        self.reasons = reasons
        self.date_time = date_time

    @staticmethod
    def is_float(str_float):
        # 判断字符串是否是小数
        str_list = str_float.split('.')
        if len(str_list) > 2 or [i for i in filter(lambda x: not x.isdigit(), str_list)]:
            return False
        else:
            return True

    @staticmethod
    def is_str_time(str_time):
        try:
            time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
            return True
        except:
            return False

    def shares_buy(self):
        sql = "select id, cost, amount, symbol from buy_already where name=%s and status=1 and user_id=%s;"
        result = execute_select_sql(database.conf, sql, self.logger, self.shares_name, self.shares_user)
        if result:
            if not(self.cost and self.amount and self.date_time):
                return 1, '输入不全'
            elif not(self.is_float(self.cost) and self.amount.isdigit() and self.is_str_time(self.date_time)):
                return 1, '价格或数量或时间输入错误'
            else:
                cnn = get_connect(database.conf)  # 获取数据库连接
                try:
                    after_cost = price_calculation(result[0][1], result[0][2], 0, float(self.cost), int(self.amount))
                    after_amount = result[0][2]+int(self.amount)
                    update_buy_already = 'update buy_already set cost=%s,amount=%s where id=%s;'
                    execute_change_sql(cnn, update_buy_already, self.logger, after_cost, after_amount, result[0][0])
                    select_surplus_money = 'select surplus_money from shares_user where id=%s;'
                    user_surplus_money = execute_select_sql(database.conf, select_surplus_money, self.logger, self.shares_user)[0][0]
                    user_surplus_money = user_surplus_money - float(self.cost)*int(self.amount)
                    update_surplus_money = 'update shares_user set surplus_money=%s where id=%s'
                    execute_change_sql(cnn, update_surplus_money, self.logger, user_surplus_money, self.shares_user)
                    insert_transaction_records = '''
                    INSERT INTO transaction_records ( user_id, hold_share_id, type, `name`, symbol, cost, amount, reasons, transaction_date ) 
                    VALUE ( %s, %s, 0, %s, %s, %s, %s, %s, %s )
                    '''
                    execute_change_sql(cnn, insert_transaction_records, self.logger, user_surplus_money, self.shares_user)


                    commit_close(cnn)    # 执行数据库并关闭连接
                except Exception as e:
                    self.logger.exception('执行更新数据库操作失败')
                    mysql_rollback(cnn)
                    return 1, '执行更新数据库操作失败'
        else:
            pass


if __name__ == '__main__':
    from shares.share_until.standard_logging import my_log
    logger = my_log()
    transaction = SharesTransactionServer(logger, 1, '杉杉股份', '16', '200', '2021-2-10 10:45:00')
    transaction.shares_buy()