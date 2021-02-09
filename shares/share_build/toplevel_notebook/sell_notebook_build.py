__author__ = '工具人'
import tkinter as tk
from tkinter import ttk


class SellNotebookBuild:
    # 生成股票操作的弹窗
    # 生成选项卡控件，注意：各个选项卡里的页面不要不直接全部生成，要触发点击选项卡事件后才生成！
    # 选项卡有：买入、卖出、交易明细、预警和日志
    def __init__(self, root, logger, shares_user, shares_name):
        self.root = root
        self.logger = logger
        self.shares_user = shares_user
        self.shares_name = shares_name
        self.sell_entry = tk.StringVar()
        self.amount_entry = tk.StringVar()
        self.year = tk.StringVar()
        self.month = tk.StringVar()
        self.day = tk.StringVar()
        self.hour = tk.StringVar()
        self.minute = tk.StringVar()

    def sell_note_build(self):
        ttk.Label(self.root, text=self.shares_name).place(relx=0.02, rely=0.02)     # 行间距 0.1
        ttk.Label(self.root, text='价格：').place(relx=0.02, rely=0.15)
        ttk.Entry(self.root, textvariable=self.sell_entry, width=8).place(relx=0.11, rely=0.15)
        ttk.Label(self.root, text='数量(股):').place(relx=0.40, rely=0.15)
        ttk.Entry(self.root, textvariable=self.amount_entry, width=8).place(relx=0.53, rely=0.15)

        ttk.Label(self.root, text='卖出时间：').place(relx=0.02, rely=0.28)

        ttk.Entry(self.root, textvariable=self.year, width=4).place(relx=0.18, rely=0.28)
        ttk.Label(self.root, text='年').place(relx=0.27, rely=0.28)      # 字到输入框 0.09， 输入框到字0.06
        ttk.Entry(self.root, textvariable=self.month, width=4).place(relx=0.33, rely=0.28)
        ttk.Label(self.root, text='月').place(relx=0.42, rely=0.28)
        ttk.Entry(self.root, textvariable=self.day, width=4).place(relx=0.48, rely=0.28)
        ttk.Label(self.root, text='日').place(relx=0.57, rely=0.28)

        ttk.Entry(self.root, textvariable=self.hour, width=4).place(relx=0.65, rely=0.28)
        ttk.Label(self.root, text='时').place(relx=0.74, rely=0.28)
        ttk.Entry(self.root, textvariable=self.minute, width=4).place(relx=0.8, rely=0.28)
        ttk.Label(self.root, text='分').place(relx=0.89, rely=0.28)

        ttk.Label(self.root, text='卖出理由：').place(relx=0.02, rely=0.41)
        tk.Text(self.root, wrap='word', height=5, width=40).place(relx=0.18, rely=0.41)
        ttk.Button(self.root, text='卖出', command='').place(relx=0.4, rely=0.8)

    def share_sell_call(self):
        pass
