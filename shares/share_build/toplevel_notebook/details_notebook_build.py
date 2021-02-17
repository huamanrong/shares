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

