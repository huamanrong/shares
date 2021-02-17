import time
from shares.share_server import database
from shares.share_until.mysql_until import *
from shares.share_until.bytecode_transformation_until import HexAndStr


class LoginServer:
    def __init__(self, account, password, logger):
        self.account = account
        self.password = password
        self.logger = logger

    def login(self):
        if not (self.account and self.password):
            return 1, '账户或密码未输入'    # 0是登录成功，1是登录失败
        elif len(self.account) > 20 or len(self.password) > 40:
            return 1, '账户或密码输入过长'
        elif [i for i in filter(lambda x: not (x.isdigit() or x.isalpha() or x == '_'), self.account)]:
            return 1, '账号只能包含数字,字母和下划线'
        elif [i for i in filter(lambda x: not (x.isdigit() or x.isalpha() or x == '_'), self.password)]:
            return 1, '密码只能只能包含数字,字母和下划线'
        elif self.account and self.password:
            conf = database.conf
            hex_str = HexAndStr()
            hex_password = hex_str.string_to_HexString(self.password)
            sql = 'select id from shares_user where name=%s and password=%s'
            result = execute_select_sql(conf, sql, self.logger, self.account, hex_password)
            if not result:
                return 1, '账户或密码错误'
            else:
                return 0, result[0][0]

    def register(self, initial_money):
        conf = database.conf
        hex_str = HexAndStr()
        hex_password = hex_str.string_to_HexString(self.password)
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
        select_sql = 'select id from shares_user where name=%s'
        res = execute_select_sql(conf, select_sql, self.logger, self.account)
        if res:
            print('用户名已注册')
        else:
            sql = 'INSERT INTO shares_user ( `name`, `password`, create_time, initial_money, surplus_money ) VALUE (%s, %s, %s, %s, %s)'
            cnn = get_connect(conf)
            execute_change_sql(cnn, sql, self.logger, self.account, hex_password, create_time, initial_money, initial_money)
            commit_close(cnn)
            print('注册成功')


if __name__ == '__main__':
    login_server = LoginServer('shanxiaojia', 'jiajia521', '')
    login_server.register(10000)
