__author__ = '工具人'
import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox
import threading


class SharesOperationToplevelBuild:
    # 生成股票操作的弹窗
    def __init__(self, root, logger):
        self.root = root
        self.logger = logger

    def shares_operation_toplevel(self):
        pass

    def shares_operation_notebook(self):
        # 生成选项卡控件，注意：各个选项卡里的页面不要不直接全部生成，要触发点击选项卡事件后才生成！
        # 选项卡有：买入、卖出、交易明细、预警和日志
        pass
