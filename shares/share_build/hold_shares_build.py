__author__ = '工具人'
import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox
import threading


class HoldSharesBuild:
    # 展示持仓记录表，使用Tree view控件，点击行弹出操作的弹窗
    def __init__(self, root, frame_page, logger):
        self.root = root
        self.frame_page = frame_page
        self.logger = logger

    def hold_shares_build(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.frame_hold_shares= ttk.Frame(self.root)
        self.frame_hold_shares.pack(expand='yes', fill=tk.BOTH)

