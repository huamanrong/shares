__author__ = '工具人'
import tkinter as tk
from tkinter import ttk


class EarlyWarningNotebookBuild:
    # 生成股票操作的弹窗
    # 生成选项卡控件，注意：各个选项卡里的页面不要不直接全部生成，要触发点击选项卡事件后才生成！
    # 选项卡有：买入、卖出、交易明细、预警和日志
    def __init__(self, root, logger, shares_user, shares_name):
        self.root = root
        self.logger = logger
        self.shares_user = shares_user
        self.shares_name = shares_name