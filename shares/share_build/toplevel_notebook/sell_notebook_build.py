__author__ = '工具人'
import time
import tkinter as tk
from tkinter import ttk, messagebox
from shares.share_server.shares_transaction_server import SharesTransactionServer
time_list = time.strftime('%Y,%m,%d,%H').split(',')


class SellNotebookBuild:
    # 生成股票操作的弹窗
    # 生成选项卡控件，注意：各个选项卡里的页面不要不直接全部生成，要触发点击选项卡事件后才生成！
    # 选项卡有：买入、卖出、交易明细、预警和日志
    def __init__(self, root, logger, shares_user, shares_name):
        self.root = root
        self.logger = logger
        self.shares_user = shares_user
        self.shares_name = shares_name
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

    def sell_note_build(self):
        ttk.Label(self.root, text=self.shares_name).place(relx=0.02, rely=0.02)     # 行间距 0.1
        ttk.Label(self.root, text='成本：').place(relx=0.02, rely=0.15)
        ttk.Entry(self.root, textvariable=self.cost_entry, width=8).place(relx=0.11, rely=0.15)
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
        self.text = tk.Text(self.root, wrap='word', height=5, width=40)
        self.text.place(relx=0.18, rely=0.41)
        self.commit_button = ttk.Button(self.root, text='卖出', command=self.share_sell_call)
        self.commit_button.place(relx=0.4, rely=0.8)

    def share_sell_call(self):
        self.commit_button['state'] = 'disabled'
        data = {'shares_name': '', 'cost': '', 'amount': '', 'reasons': '', 'date_time': '', 'stop_loss_price': '', 'stop_profit_price': '',
                'stop_profit_after_high_falls_proportion': ''}
        date_time = '%s-%s-%s %s:%s:00' % (self.year.get(), self.month.get(), self.day.get(), self.hour.get(), self.minute.get())
        data['shares_name'] = self.shares_name
        data['cost'] = self.cost_entry.get()
        data['amount'] = self.amount_entry.get()
        data['reasons'] = self.text.get(index1='1.0', index2='end')
        data['date_time'] = date_time
        print(data)
        result = SharesTransactionServer(self.logger, self.shares_user).shares_sell(data)
        if result[0]:
            messagebox.showwarning('卖出提示', result[1])
            self.commit_button['state'] = 'normal'
        else:
            messagebox.showinfo('卖出提示', result[1])
            self.clear_input()
            self.commit_button['state'] = 'normal'

    def clear_input(self):
        self.cost_entry.set('')
        self.amount_entry.set('')
        self.minute.set('')
        self.text.delete(index1='1.0', index2='end')
