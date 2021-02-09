__author__ = '工具人'
import tkinter as tk
from tkinter import ttk
from shares.share_build.toplevel_notebook.buy_notebook_build import BuyNotebookBuild
from shares.share_build.toplevel_notebook.sell_notebook_build import SellNotebookBuild


class SharesOperationNotebookBuild:
    # 生成股票操作的弹窗
    # 生成选项卡控件，注意：各个选项卡里的页面不要不直接全部生成，要触发点击选项卡事件后才生成！
    # 选项卡有：买入、卖出、交易明细、预警和日志
    def __init__(self, root, logger, shares_user, shares_name):
        self.root = root
        self.logger = logger
        self.shares_user = shares_user
        self.shares_name = shares_name

    def shares_operation_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand="yes")
        self.frame_buy = ttk.Frame(self.notebook)
        self.frame_sell = ttk.Frame(self.notebook)
        self.frame_early_waining = ttk.Frame(self.notebook)
        self.frame_details = ttk.Frame(self.notebook)
        self.frame_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_buy, text="    买入    ")
        self.notebook.add(self.frame_sell, text="    卖出    ")
        self.notebook.add(self.frame_early_waining, text="    预警    ")
        self.notebook.add(self.frame_details, text=" 交易明细 ")
        self.notebook.add(self.frame_logs, text="    日志    ")
        BuyNotebookBuild(self.frame_buy, self.logger, self.shares_user, self.shares_name).buy_note_build()
        SellNotebookBuild(self.frame_sell, self.logger, self.shares_user, self.shares_name).sell_note_build()

