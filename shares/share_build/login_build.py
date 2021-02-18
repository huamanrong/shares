__author__ = '工具人'
import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox
from shares.share_until.standard_logging import my_log
from shares.share_server.login_server import LoginServer
from shares.share_build.hold_shares_build import HoldSharesBuild


class LoginBuild:
    def __init__(self, root):
        self.root = root
        style = ttk.Style()
        style.configure('Treeview', rowheight=25)
        style.theme_use("vista")
        self.root.title('股票管理')
        self.root.geometry("500x400+700+200")
        self.root.resizable(0, 0)
        self.frame_page = {'frame': None}
        self.logger = my_log()
        self.shares_user = None
        self.account = tk.StringVar()
        self.password = tk.StringVar()
        # self.account.set('xiaohu')
        # self.password.set('123456')
        self.login_build()

    def login_build(self):
        self.frame_login = tk.Frame(self.root)
        self.frame_page['frame'] = self.frame_login
        self.frame_login.pack(expand='yes', fill=tk.BOTH)
        ttk.Label(self.frame_login, text='管理帐号:').place(relx=0.3, rely=0.3)
        ttk.Entry(self.frame_login, width=20, textvariable=self.account).place(relx=0.43, rely=0.3)
        ttk.Label(self.frame_login, text='管理密码:').place(relx=0.3, rely=0.45)
        ttk.Entry(self.frame_login, show='*', width=20, textvariable=self.password).place(relx=0.43, rely=0.45)
        self.login_button = ttk.Button(self.frame_login, text='登录', command=self.login)
        self.login_button.place(relx=0.42, rely=0.6)
        self.root.bind('<Return>', self.login_return_callback)
        ttk.Label(self.frame_login, text='作者：工具人').place(relx=0.8, rely=0.9)

    def login_return_callback(self, event):
        self.login()

    def login(self):
        self.login_button['state'] = 'disabled'
        login_obj = LoginServer(self.account.get(), self.password.get(), self.logger)
        response = login_obj.login()
        if response[0]:
            messagebox.showwarning('登录提示', response[1])
            self.login_button['state'] = 'normal'
        else:
            self.shares_user = response[1]
            self.frame_login.destroy()
            self.root.unbind('<Return>')
            self.menu_page()

    def again_login(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.menu_bar.destroy()
        self.login_build()

    def quit(self):
        self.root.destroy()

    def menu_page(self):
        self.menu_bar = Menu(self.root)
        self.root["menu"] = self.menu_bar
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='菜单', menu=file_menu)
        file_menu.add_command(label='重新登录', command=self.again_login)
        file_menu.add_separator()
        file_menu.add_command(label='退出程序', command=self.quit)

        hold_share = HoldSharesBuild(self.root, self.frame_page, self.shares_user, self.logger)
        operation_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='股票操作', menu=operation_menu)
        operation_menu.add_command(label='持仓', command=hold_share.hold_shares_build)
        operation_menu.add_command(label='买入', command='')
        operation_menu.add_command(label='卖出', command='')
        operation_menu.add_command(label='已清仓', command='')

        early_warning_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='股票预警', menu=early_warning_menu)
        early_warning_menu.add_command(label='添加预警', command='')
        early_warning_menu.add_command(label='预警列表', command='')

        plan_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='计划', menu=plan_menu)
        plan_menu.add_command(label='近期操作计划', command='')
        plan_menu.add_command(label='股票池', command='')

        log_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='股票日志', menu=log_menu)
        log_menu.add_command(label='添加日志', command='')
        log_menu.add_command(label='日志列表', command='')

        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='帮助', menu=help_menu)
        help_menu.add_command(label='关于', command='')
        hold_share.hold_shares_build()


if __name__ == '__main__':
    master = tk.Tk()
    LoginBuild(master)
    master.mainloop()
