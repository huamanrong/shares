__author__ = '工具人'
import tkinter as tk
from tkinter import ttk
from shares.share_until.creat_thread import create_thread
from shares.share_server.hold_shares_lists_server import HoldSharesListsServer


class HoldSharesBuild:
    # 展示持仓记录表，使用Tree view控件，点击行弹出操作的弹窗
    def __init__(self, root, frame_page, shares_user, logger):
        self.root = root
        self.root.geometry("600x380+700+200")
        self.frame_page = frame_page
        self.shares_user = shares_user
        self.logger = logger
        self.items_value = {}

    def hold_shares_build(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.frame_hold_shares= ttk.Frame(self.root)
        self.frame_hold_shares.pack(expand='yes', fill=tk.BOTH)
        self.tree = ttk.Treeview(self.frame_hold_shares, show='headings', height=20, columns=['0', '1', '2', '3', '4', '5'])
        self.tree.bind("<<TreeviewSelect>>", self.trigger_call_toplevel)     # 监听tree中item被选中的事件
        self.tree.heading(0, text='名称')
        self.tree.heading(1, text='盈亏')
        self.tree.heading(2, text='成本/现价')
        self.tree.heading(3, text='持仓')
        self.tree.heading(4, text='当日盈亏')
        self.tree.heading(5, text='仓位')

        # 设置每列中元素的样式, center为居中，可选的参数为w e s n
        self.tree.column(0, anchor='center', width=100)
        self.tree.column(1, anchor='center', width=100)
        self.tree.column(2, anchor='center', width=100)
        self.tree.column(3, anchor='center', width=100)
        self.tree.column(4, anchor='center', width=100)
        self.tree.column(5, anchor='center', width=100)
        # self.tree.insert("", 'end', values=(1, 2, 3))
        # print('tree')
        create_thread(self.update_tree_items_loop)

    def set_tree_items(self, queue_value):
        items = self.tree.get_children()
        [self.tree.delete(item) for item in items]
        self.tree.update()
        for index, item in enumerate(queue_value):
            self.tree.insert("", index, values=item)
        self.tree.pack()

    def update_tree_items_loop(self):
        hold_server = HoldSharesListsServer(self.shares_user, self.logger)
        hold_server.get_items_value()
        while '工具人':
            queue_value = hold_server.work_queue.get()
            print(queue_value)
            queue_value.work_queue.task_done()
            if queue_value:
                self.set_tree_items(queue_value)
                print('update_tree_items_loop')

    def trigger_call_toplevel(self, *args):
        pass
