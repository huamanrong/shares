from shares.share_server import database
from shares.share_until.mysql_until import *


class LoginServer:
    def __init__(self, account, password, logger):
        self.account = account
        self.password = password
        self.logger = logger

    def login(self):
        if not (self.account and self.password):
            return 1, '账户或密码未输入'    # 0是登录成功，1是登录失败
        elif len(self.account) > 20 or len(self.password) > 20:
            return 1, '账户或密码未输入'
        elif self.account and self.password:
            conf = database.conf
            sql = 'select id from user where name="%s" and password="%s"' % (self.account, self.password)
            result = execute_select_sql(conf, sql, self.logger)
            if not result:
                return 1, '账户或密码错误'
            else:
                return 0, result[0][0]
