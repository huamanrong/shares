# 菜单的买入页面
__author__ = '工具人'
import time
import tkinter as tk
from tkinter import ttk, messagebox
from shares.share_server.shares_transaction_server import SharesTransactionServer
time_list = time.strftime('%Y,%m,%d,%H').split(',')


class SharesOperationBuyBuild:
    # 生成股票操作的弹窗
    # 生成选项卡控件，注意：各个选项卡里的页面不要不直接全部生成，要触发点击选项卡事件后才生成！
    # 选项卡有：买入、卖出、交易明细、预警和日志
    def __init__(self, root, frame_page, shares_user, logger):
        self.root = root
        self.logger = logger
        self.shares_user = shares_user
        self.frame_page = frame_page
        self.shares_name = tk.StringVar()
        self.cost_entry = tk.StringVar()
        self.amount_entry = tk.StringVar()
        self.year = tk.StringVar()
        self.month = tk.StringVar()
        self.day = tk.StringVar()
        self.hour = tk.StringVar()
        self.minute = tk.StringVar()
        self.year.set(time_list[0])
        self.month.set(time_list[1])
        self.day.set(time_list[2])
        self.hour.set(time_list[3])

    def shares_operation_buy_build(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.frame_buy = ttk.Frame(self.root)
        self.frame_page['frame'] = self.frame_buy
        self.frame_buy.pack(expand='yes', fill=tk.BOTH)
        ttk.Label(self.root, text='股票名称或代码：').place(relx=0.02, rely=0.04)
        ttk.Entry(self.root, textvariable=self.shares_name, width=8).place(relx=0.19, rely=0.04)
        ttk.Label(self.root, text='成本：').place(relx=0.02, rely=0.15)
        ttk.Entry(self.root, textvariable=self.cost_entry, width=8).place(relx=0.09, rely=0.15)
        ttk.Label(self.root, text='数量(股):').place(relx=0.26, rely=0.15)
        ttk.Entry(self.root, textvariable=self.amount_entry, width=8).place(relx=0.35, rely=0.15)

        ttk.Label(self.root, text='买入时间：').place(relx=0.02, rely=0.28)

        ttk.Entry(self.root, textvariable=self.year, width=4).place(relx=0.14, rely=0.28)
        ttk.Label(self.root, text='年').place(relx=0.21, rely=0.28)      # 字到输入框 0.05， 输入框到字0.07
        ttk.Entry(self.root, textvariable=self.month, width=4).place(relx=0.26, rely=0.28)
        ttk.Label(self.root, text='月').place(relx=0.33, rely=0.28)
        ttk.Entry(self.root, textvariable=self.day, width=4).place(relx=0.38, rely=0.28)
        ttk.Label(self.root, text='日').place(relx=0.45, rely=0.28)

        ttk.Entry(self.root, textvariable=self.hour, width=4).place(relx=0.5, rely=0.28)
        ttk.Label(self.root, text='时').place(relx=0.57, rely=0.28)
        ttk.Entry(self.root, textvariable=self.minute, width=4).place(relx=0.62, rely=0.28)
        ttk.Label(self.root, text='分').place(relx=0.69, rely=0.28)

        ttk.Label(self.root, text='买入理由：').place(relx=0.02, rely=0.41)
        self.text = tk.Text(self.root, wrap='word', height=7, width=50)
        self.text.place(relx=0.14, rely=0.41)
        self.commit_button = ttk.Button(self.root, text='买入', command=self.share_buy_call)
        self.commit_button.place(relx=0.4, rely=0.8)

    def share_buy_call(self):
        self.commit_button['state'] = 'disabled'
        data = {'shares_name': '', 'cost': '', 'amount': '', 'reasons': '', 'date_time': '', 'stop_loss_price': '', 'stop_profit_price': '',
                'stop_profit_after_high_falls_proportion': ''}
        date_time = '%s-%s-%s %s:%s:00' % (self.year.get(), self.month.get(), self.day.get(), self.hour.get(), self.minute.get())
        data['shares_name'] = self.shares_name.get()
        data['cost'] = self.cost_entry.get()
        data['amount'] = self.amount_entry.get()
        data['reasons'] = self.text.get(index1='1.0', index2='end')
        data['date_time'] = date_time
        print(data)
        result = SharesTransactionServer(self.logger, self.shares_user).shares_buy_menu(data)
        if result[0]:
            messagebox.showwarning('买入提示', result[1])
            self.commit_button['state'] = 'normal'
        else:
            messagebox.showinfo('买入提示', result[1])
            self.clear_input()
            self.commit_button['state'] = 'normal'

    def clear_input(self):
        self.shares_name.set('')
        self.cost_entry.set('')
        self.amount_entry.set('')
        self.minute.set('')
        self.text.delete(index1='1.0', index2='end')