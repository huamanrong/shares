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
        elif len(self.account) > 20 or len(self.password) > 20:
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


if __name__ == '__main__':
    pass
