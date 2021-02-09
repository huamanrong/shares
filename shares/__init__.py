__author__ = '工具人'
import tkinter as tk
from tkinter import messagebox
from shares.share_build.login_build import LoginBuild


def on_closing():
    # if messagebox.askokcancel("退出", "确定要退出？"):
        root.destroy()
    # pass


if __name__ == '__main__':
    'https://tushare.pro/document/2'
    root = tk.Tk()
    login = LoginBuild(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
