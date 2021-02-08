__author__ = '工具人'
import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox
import threading


class HoldSharesBuild:
    # 展示持仓记录表，使用Tree view控件，点击行弹出操作的弹窗
    def __init__(self, root, frame_page, logger):
        self.root = root
        self.root.geometry("600x380+700+200")
        self.frame_page = frame_page
        self.logger = logger

    def hold_shares_build(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.frame_hold_shares= ttk.Frame(self.root)
        self.frame_hold_shares.pack(expand='yes', fill=tk.BOTH)
        tree = ttk.Treeview(self.frame_hold_shares, show='headings', height=20, columns=['0', '1', '2', '3', '4', '5'])
        tree.bind("<<TreeviewSelect>>", self.trigger_call_toplevel)     # 监听tree中item被选中的事件
        tree.heading(0, text='名称')
        tree.heading(1, text='盈亏')
        tree.heading(2, text='成本/现价')
        tree.heading(3, text='持仓')
        tree.heading(4, text='当日盈亏')
        tree.heading(5, text='仓位')

        # 设置每列中元素的样式, center为居中，可选的参数为w e s n
        tree.column(0, anchor='center', width=100)
        tree.column(1, anchor='center', width=100)
        tree.column(2, anchor='center', width=100)
        tree.column(3, anchor='center', width=100)
        tree.column(4, anchor='center', width=100)
        tree.column(5, anchor='center', width=100)

        # "end" 表示往父节点的最后一个位置插入
        tree.insert("", "end", values=("1", "赵二", "19"))
        tree.insert("", "end", values=("2", "张三", "20"))
        tree.insert("", "end", values=("3", "李四", "22"))
        tree.insert("", "end", values=("4", "王五", "18"))
        tree.insert("", "end", values=("1", "赵二", "19"))
        tree.insert("", "end", values=("2", "张三", "20"))
        tree.insert("", "end", values=("3", "李四", "22"))
        tree.insert("", "end", values=("4", "王五", "18"))
        tree.insert("", "end", values=("1", "赵二", "19"))
        tree.insert("", "end", values=("2", "张三", "20"))
        tree.insert("", "end", values=("3", "李四", "22"))
        tree.insert("", "end", values=("4", "王五", "18"))
        tree.insert("", "end", values=("1", "赵二", "19"))
        tree.insert("", "end", values=("2", "张三", "20"))
        tree.pack()

    def trigger_call_toplevel(self, *args):
        pass