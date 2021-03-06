import time
from shares.share_until.mysql_until import *
from shares.share_server import database
from shares.share_until.shares_calculation import *


class SharesTransactionServer:
    def __init__(self, logger, shares_user):
        self.logger = logger
        self.shares_user = shares_user

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

    def shares_buy_hold_list(self, data):   # 通过持仓列表的操作进行买入
        # data = {'shares_name': '', 'cost': '', 'amount': '', 'reasons': '', 'date_time': '', 'stop_loss_price': '', 'stop_profit_price': '',
        #         'stop_profit_after_high_falls_proportion': ''}
        if not (data['cost'] and data['amount'] and data['date_time'] and data['shares_name']):
            return 1, '输入不全'
        elif not (self.is_float(data['cost']) and data['amount'].isdigit() and self.is_str_time(data['date_time'])):
            return 1, '价格、数量或时间输入错误'
        select_surplus_money = 'select surplus_money from shares_user where id=%s;'
        user_surplus_money = execute_select_sql(database.conf, select_surplus_money, self.logger, self.shares_user)[0][0]
        if float(data['cost']) * int(data['amount']) > user_surplus_money:
            return 1, '买入金额大于用户剩余金额'
        sql = "select id, cost, amount, symbol, real_cost from buy_already where name=%s and status=1 and user_id=%s ;"
        result = execute_select_sql(database.conf, sql, self.logger, data['shares_name'], self.shares_user)
        cnn = get_connect(database.conf)  # 获取数据库连接
        try:
            after_cost = price_calculation(result[0][1], result[0][2], 0, float(data['cost']), int(data['amount']))
            after_real_cost = price_calculation(result[0][4], result[0][2], 0, float(data['cost']), int(data['amount']))
            after_amount = result[0][2]+int(data['amount'])
            update_buy_already = 'update buy_already set cost=%s,real_cost=%s, amount=%s where id=%s;'    # 更新持仓表
            execute_change_sql(cnn, update_buy_already, self.logger, after_cost, after_real_cost, after_amount, result[0][0])
            user_surplus_money = user_surplus_money - float(data['cost'])*int(data['amount'])
            update_surplus_money = 'update shares_user set surplus_money=%s where id=%s'    # 更新用户表，剩余金额字段
            execute_change_sql(cnn, update_surplus_money, self.logger, user_surplus_money, self.shares_user)

            insert_transaction_records = '''
            INSERT INTO transaction_records ( user_id, hold_share_id, type, `name`, symbol, cost, amount, reasons, transaction_date ) 
            VALUE ( %s, %s, 0, %s, %s, %s, %s, %s, %s )
            '''
            execute_change_sql(cnn, insert_transaction_records, self.logger, self.shares_user, result[0][0], data['shares_name'], result[0][3], data['cost'],
                               data['amount'], data['reasons'], data['date_time'])      # 插入买入记录
            commit_close(cnn)    # 执行数据库并关闭连接
            return 0, '买入成功'
        except:
            self.logger.exception('执行更新数据库操作失败')
            mysql_rollback(cnn)     # 如果执行报错就回滚并关闭数据库
            return 1, '执行更新数据库操作失败'
        # 更新预警列表数据

    def shares_buy_menu(self, data):   # 通过菜单的操作进行买入
        # data = {'shares_name': '', 'cost': '', 'amount': '', 'reasons': '', 'date_time': '', 'stop_loss_price': '', 'stop_profit_price': '',
        #         'stop_profit_after_high_falls_proportion': ''}
        if not (data['cost'] and data['amount'] and data['date_time'] and data['shares_name']):
            return 1, '输入不全'
        elif not (self.is_float(data['cost']) and data['amount'].isdigit() and self.is_str_time(data['date_time'])):
            return 1, '价格、数量或时间输入错误'
        elif data['stop_loss_price'] and not self.is_float(data['stop_loss_price']):
            return 1, '止损比例输入错误'
        elif data['stop_profit_price'] and not self.is_float(data['stop_profit_price']):
            return 1, '止盈比例输入错误'
        elif data['stop_profit_after_high_falls_proportion'] and not self.is_float(data['stop_profit_after_high_falls_proportion']):
            return 1, '由上而下止盈比例输入错误'
        select_symbol = 'SELECT `name`, symbol FROM all_shares WHERE `name`=%s or symbol=%s;'  # 查询输入的股票是否存在并获得名称和代码
        symbol_result = execute_select_sql(database.conf, select_symbol, self.logger, data['shares_name'], data['shares_name'])
        if not symbol_result:
            return 1, '股票名称或代码输入错误'
        select_surplus_money = 'select surplus_money from shares_user where id=%s;'
        user_surplus_money = execute_select_sql(database.conf, select_surplus_money, self.logger, self.shares_user)[0][0]
        if float(data['cost']) * int(data['amount']) > user_surplus_money:
            return 1, '买入金额大于用户剩余金额'
        sql = "select id, cost, amount, symbol, stop_loss_price, stop_profit_price, stop_profit_after_high_falls_proportion, real_cost from buy_already where " \
              "name=%s or symbol=%s and status=1 and user_id=%s ;"
        result = execute_select_sql(database.conf, sql, self.logger, data['shares_name'], data['shares_name'], self.shares_user)
        cnn = get_connect(database.conf)  # 获取数据库连接
        stop_loss_price = float(data['stop_loss_price']) if data['stop_loss_price'] else None
        stop_profit_price = float(data['stop_profit_price']) if data['stop_profit_price'] else None
        stop_profit_after_high_falls_proportion = float(data['stop_profit_after_high_falls_proportion']) if data['stop_profit_after_high_falls_proportion'] else None
        try:
            if result:
                after_cost = price_calculation(result[0][1], result[0][2], 0, float(data['cost']), int(data['amount']))
                after_real_cost = price_calculation(result[0][7], result[0][2], 0, float(data['cost']), int(data['amount']))
                after_amount = result[0][2]+int(data['amount'])
                stop_loss_price = stop_loss_price if stop_loss_price else result[0][4]
                stop_profit_price = stop_profit_price if stop_profit_price else result[0][5]
                stop_profit_after_high_falls_proportion = stop_profit_after_high_falls_proportion if stop_profit_after_high_falls_proportion else result[0][6]
                update_buy_already = 'update buy_already set cost=%s,real_cost=%s,amount=%s,stop_loss_price=%s,stop_profit_price=%s,stop_profit_after_high_falls_proportion=%s ' \
                                     'where id=%s;'
                execute_change_sql(cnn, update_buy_already, self.logger, after_cost, after_real_cost, after_amount, stop_loss_price, stop_profit_price,
                                   stop_profit_after_high_falls_proportion, result[0][0])

                insert_transaction_records = '''
                INSERT INTO transaction_records ( user_id, hold_share_id, type, `name`, symbol, cost, amount, reasons, transaction_date ) 
                VALUE ( %s, %s, 0, %s, %s, %s, %s, %s, %s )
                '''
                execute_change_sql(cnn, insert_transaction_records, self.logger, self.shares_user, result[0][0], data['shares_name'], result[0][3], data['cost'],
                                   data['amount'], data['reasons'], data['date_time'])
            else:
                insert_buy_already = 'INSERT INTO buy_already ( user_id, `name`, symbol, cost, real_cost, amount, buying_reasons, stop_loss_price, stop_profit_price, ' \
                                     'stop_profit_after_high_falls_proportion, buy_datetime, `status` ) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)'
                insert_id = execute_change_sql(cnn, insert_buy_already, self.logger, self.shares_user, symbol_result[0][0], symbol_result[0][1], float(data['cost']),
                                               float(data['cost']), int(data['amount']), data['reasons'], stop_loss_price, stop_profit_price,
                                               stop_profit_after_high_falls_proportion, data['date_time'])

                insert_transaction_records = '''
                            INSERT INTO transaction_records ( user_id, hold_share_id, type, `name`, symbol, cost, amount, reasons, transaction_date ) 
                            VALUE ( %s, %s, 0, %s, %s, %s, %s, %s, %s )
                            '''
                execute_change_sql(cnn, insert_transaction_records, self.logger, self.shares_user, insert_id, symbol_result[0][0], symbol_result[0][1], float(data['cost']),
                                   int(data['amount']), data['reasons'], data['date_time'])
            user_surplus_money = user_surplus_money - float(data['cost']) * int(data['amount'])
            update_surplus_money = 'update shares_user set surplus_money=%s where id=%s'
            execute_change_sql(cnn, update_surplus_money, self.logger, user_surplus_money, self.shares_user)
            commit_close(cnn)  # 执行数据库并关闭连接
            return 0, '买入成功'
        except:
            self.logger.exception('执行更新数据库操作失败')
            mysql_rollback(cnn)     # 如果执行报错就回滚并关闭数据库
            return 1, '执行更新数据库操作失败'
        # 更新预警列表数据

    def shares_sell(self, data):
        # data = {'shares_name': '', 'cost': '', 'amount': '', 'reasons': '', 'date_time': ''}
        if not (data['cost'] and data['amount'] and data['date_time'] and data['shares_name']):
            return 1, '输入不全'
        elif not (self.is_float(data['cost']) and data['amount'].isdigit() and self.is_str_time(data['date_time'])):
            return 1, '价格、数量或时间输入错误'
        sql = "select id, cost, amount, name, symbol, real_cost from buy_already where name=%s or symbol=%s and status=1 and user_id=%s ;"
        result = execute_select_sql(database.conf, sql, self.logger, data['shares_name'], data['shares_name'], self.shares_user)
        cnn = get_connect(database.conf)  # 获取数据库连接
        try:
            if result:
                if result[0][2] < int(data['amount']):
                    return 1, '卖出数量大于剩余股票数量'
                after_amount = result[0][2] - int(data['amount'])
                status = 1 if after_amount > 0 else 0
                after_cost = price_calculation(result[0][1], result[0][2], 1, float(data['cost']), int(data['amount'])) if after_amount > 0 else result[0][1]

                update_buy_already = 'update buy_already set cost=%s, amount=%s, status=%s where id=%s;'
                execute_change_sql(cnn, update_buy_already, self.logger, after_cost, after_amount, status, result[0][0])

                select_surplus_money = 'select surplus_money from shares_user where id=%s;'
                user_surplus_money = execute_select_sql(database.conf, select_surplus_money, self.logger, self.shares_user)[0][0]
                user_surplus_money = user_surplus_money + float(data['cost']) * int(data['amount'])
                update_surplus_money = 'update shares_user set surplus_money=%s where id=%s'
                execute_change_sql(cnn, update_surplus_money, self.logger, user_surplus_money, self.shares_user)
                after_real_cost = result[0][5]
                selling_profit = (float(data['cost']) - after_real_cost) * int(data['amount'])
                insert_transaction_records = '''
                        INSERT INTO transaction_records ( user_id, hold_share_id, type, `name`, symbol, selling_price, amount, selling_profit, reasons, transaction_date) 
                        VALUE ( %s, %s, 1, %s, %s, %s, %s, %s, %s, %s)
                        '''
                execute_change_sql(cnn, insert_transaction_records, self.logger, self.shares_user, result[0][0], result[0][3], result[0][4], float(data['cost']),
                                   int(data['amount']), selling_profit, data['reasons'], data['date_time'])
                commit_close(cnn)  # 执行数据库并关闭连接
                return 0, '卖出成功'
            else:
                return 1, '该股票还未买入不能卖出'
        except:
            self.logger.exception('执行更新数据库操作失败')
            mysql_rollback(cnn)  # 如果执行报错就回滚并关闭数据库
            return 1, '执行更新数据库操作失败'
        # 更新预警列表数据

    def update_early_warning(self):
        pass


if __name__ == '__main__':
    # from shares.share_until.standard_logging import my_log
    # logger = my_log()
    # transaction = SharesTransactionServer(logger, 1, '杉杉股份', '16', '200', '2021-2-10 10:45:00')
    # transaction.shares_buy()
    print('-5'.isdigit())
    pass
