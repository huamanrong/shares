from shares.share_until.mysql_until import *
from shares.share_server import database


class SharesTransactionServer:
    def __init__(self, logger, shares_user, shares_name, cost, amount, date_time):
        self.logger = logger
        self.shares_user = shares_user
        self.shares_name = shares_name
        self.cost = cost
        self.amount = amount
        self.date_time = date_time

    def shares_buy(self):
        sql = "select id, cost, amount from buy_already where name=%s and status=1;"
        result = execute_select_sql(database.conf, sql, self.logger, self.shares_name)
        if result:
            pass
        else:
            pass
