__author__ = '工具人'
import tkinter as tk
from tkinter import ttk


class DetailsNotebookBuild:
    # 生成股票操作的弹窗
    # 生成选项卡控件，注意：各个选项卡里的页面不要不直接全部生成，要触发点击选项卡事件后才生成！
    # 选项卡有：买入、卖出、交易明细、预警和日志
    def __init__(self, root, logger, shares_user, shares_name):
        self.root = root
        self.logger = logger
        self.shares_user = shares_user
        self.shares_name = shares_name

    def details_notebook_build(self):
        self.canvas = tk.Canvas(self.root)  # , width=500, height=500, scrollregion=(0, 0, 500, 400)
        self.canvas.pack(fill='both', expand=1)
        # 滚动条
        ysb = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=ysb.set)
        ysb.pack(side='right', fill='y')
        # !!!!=======重点：鼠标滚轮滚动时，改变的页面是canvas 而不是treeview
        self.canvas.bind_all("<MouseWheel>",
                             lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # from tkinter import *
        #
        # main_page = Tk()
        # main_page.geometry("400x300")
        # cv_mian = Canvas(main_page, scrollregion=(0, 0, 400, 600))
        # cv_mian.pack(expand='yes', fill=BOTH)
        # frame1 = Frame(cv_mian)
        # frame1.pack(side=LEFT, fill=BOTH)
        #
        # vbar = Scrollbar(cv_mian, orient=VERTICAL, command=cv_mian.yview)  # 竖直滚动条
        # vbar.pack(side=RIGHT, fill=Y)
        # cv_mian.configure(yscrollcommand=vbar.set)
        #
        # cv_mian.bind_all("<MouseWheel>", lambda event: cv_mian.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        # cv_mian.create_window(0, 0, window=frame1, anchor='nw', width=400, height=1000)
        # main_page.resizable()
        # for i in range(20):
        #     Label(frame1, text='%s' % i).grid()
        # main_page.mainloop()

