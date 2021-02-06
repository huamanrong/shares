__author__ = '工具人'
import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox
import threading
from shares.share_until.standard_logging import my_log
from shares.share_server.login_server import LoginServer


class LoginBuild:
    def __init__(self, root):
        self.root = root
        self.root.title('股票管理')
        self.root.geometry("500x400+700+200")
        self.root.resizable(0, 0)
        self.frame_page = {'frame': None}
        self.logger = my_log()
        self.account = tk.StringVar()
        self.password = tk.StringVar()
        self.login_build()

    @staticmethod
    def create_thread(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def login_build(self):
        self.frame_login = tk.Frame(self.root)
        self.frame_page['frame'] = self.frame_login
        self.frame_login.pack(expand='yes', fill=tk.BOTH)
        ttk.Label(self.frame_login, text='管理帐号:').place(relx=0.3, rely=0.3)
        ttk.Entry(self.frame_login, width=20, textvariable=self.account).place(relx=0.43, rely=0.3)
        ttk.Label(self.frame_login, text='管理密码:').place(relx=0.3, rely=0.45)
        ttk.Entry(self.frame_login, show='*', width=20, textvariable=self.password).place(relx=0.43, rely=0.45)
        login_button = ttk.Button(self.frame_login, text='登录', command=self.login)
        login_button.place(relx=0.42, rely=0.6)
        self.root.bind('<Return>', self.login_return_callback)
        ttk.Label(self.frame_login, text='作者：工具人').place(relx=0.8, rely=0.9)

    def login_return_callback(self, event):
        self.login()

    def login(self):
        login_obj = LoginServer(self.account.get(), self.password.get())
        login_obj.login()

    def again_login(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.menu_bar.destroy()
        self.login_build()

    def menu_page(self):
        self.menu_bar = Menu(self.root)
        self.root["menu"] = self.menu_bar
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='菜单', menu=file_menu)
        file_menu.add_command(label='重新登录', command=self.again_login)
        file_menu.add_command(label='退出程序', command=self.quit)

        function_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='功能', menu=function_menu)
        function_menu.add_command(label='股票预警', command='')

    def quit(self):
        self.root.destroy()


if __name__ == '__main__':
    master = tk.Tk()
    LoginBuild(master)
    master.mainloop()
