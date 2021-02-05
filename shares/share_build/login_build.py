__author__ = '工具人'
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
from shares.share_until.standard_logging import my_log
logger = my_log()


class LoginBuild:
    def __init__(self, root):
        self.root = root
        self.frame_page = {'frame': ''}
        self.login_build()

    @staticmethod
    def create_thread(func, *args):
        # 将函数打包进线程
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def login_build(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.frame_login = tk.Frame(self.root)
        self.frame_page['frame'] = self.frame_login
        self.frame_login.pack(expand='yes', fill=tk.BOTH)
        ttk.Label(self.frame_login, text='作者：工具人').pack(anchor='e', side='bottom', ipadx=5)


if __name__ == '__main__':
    master = tk.Tk()
    LoginBuild(master)
    master.mainloop()
