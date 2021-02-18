__author__ = '工具人'
import time
# import Pmw  # tkinter扩展包，需要导入
import tkinter as tk
from tkinter import ttk
from shares.share_until.creat_thread import create_thread
from shares.share_server.hold_shares_lists_server import HoldSharesListsServer
from shares.share_build.toplevel_notebook.shares_operation_notebook_build import SharesOperationNotebookBuild


class HoldSharesBuild:
    # 展示持仓记录表，使用Tree view控件，点击行弹出操作的弹窗
    def __init__(self, root, frame_page, shares_user, logger):
        self.root = root
        self.root.geometry("610x380+700+200")
        self.frame_page = frame_page
        self.shares_user = shares_user
        self.logger = logger
        self.items_Toplevel = {}

    def hold_shares_build(self):
        if self.frame_page['frame']:
            self.frame_page['frame'].destroy()
        self.frame_hold_shares= ttk.Frame(self.root)
        self.frame_page['frame'] = self.frame_hold_shares
        self.frame_hold_shares.pack(expand='yes', fill=tk.BOTH)
        y_bar = ttk.Scrollbar(self.frame_hold_shares, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self.frame_hold_shares, show='headings', height=20, columns=['0', '1', '2', '3', '4', '5'], yscrollcommand=y_bar.set)
        y_bar['command'] = self.tree.yview
        y_bar.pack(side='right', fill='y')
        self.tree.bind("<Double-Button-1>", self.trigger_call_toplevel)     # 监听tree中item双击事件
        # self.tree.bind("<Enter>", self.tips_window)     # 监听鼠标移动到Tree view区域事件
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
        self.tree.pack(expand=1, fill='both')
        create_thread(self.update_tree_items_loop)

    # def tips_window(self, *args):
    #     balloon = Pmw.Balloon(self.frame_hold_shares)
    #     balloon.bind(self.tree, '双击进行股票操作')

    def set_tree_items(self, queue_value):
        items = self.tree.get_children()
        if not self.tree.get_children():    # 一开始列表没有数据，就插入
            for index, item in enumerate(queue_value):
                self.tree.insert("", index, values=item)
        elif len(items) != len(queue_value):
            [self.tree.delete(item) for item in items]
            for index, item in enumerate(queue_value):
                self.tree.insert("", index, values=item)
        else:       # 有数据就修改，不进行删除
            for index_1, item_1 in enumerate(items):
                for index_2 in range(len(queue_value[0])):
                    self.tree.set(item_1, index_2, queue_value[index_1][index_2])

    def update_tree_items_loop(self):
        hold_server = HoldSharesListsServer(self.shares_user, self.logger)
        while '工具人':
            hold_server.get_items_value()
            queue_value = hold_server.work_queue.get()
            print('queue_value', queue_value)
            hold_server.work_queue.task_done()
            # if queue_value:
            self.set_tree_items(queue_value)
            time.sleep(10)

    def on_closing(self):   # 子窗口关闭的回调函数
        del self.items_Toplevel[self.window]
        self.window.destroy()

    def trigger_call_toplevel(self, *args):
        # 单列的弹窗只触发一次,重复点击单列不会创建新的弹窗
        # 最多有1个弹窗
        if not self.items_Toplevel:
            self.toplevel_build()
        elif self.tree.focus() not in self.items_Toplevel.values():
            self.window.destroy()
            del self.items_Toplevel[self.window]
            self.toplevel_build()

    def toplevel_build(self, *args):
        self.window = tk.Toplevel(self.frame_hold_shares)
        self.items_Toplevel[self.window] = self.tree.focus()
        screenwidth = self.root.winfo_screenwidth()  # 获取屏幕的宽度，高度是 winfo_screenheight
        main_x, main_y = self.root.winfo_x(), self.root.winfo_y()  # 获取主窗口的坐标
        main_width, main_height = self.root.winfo_width(), self.root.winfo_height()  # 获取主窗口的宽度，高度
        if screenwidth > main_x + main_width + 400:     # 主窗口右边空间足够，弹窗就展示在右边，不够的话就弹窗展示在主窗口左边
            self.window.geometry("400x300+%s+%s" % (int(main_x + main_width+5), int(main_y)))
        else:
            self.window.geometry("400x300+%s+%s" % (int(main_x - 400 - 5), int(main_y)))

        select_item = self.tree.item(self.tree.selection(), "values")

        self.window.title(select_item[0])
        shares_notebook = SharesOperationNotebookBuild(self.window, self.logger, self.shares_user, select_item[0])
        shares_notebook.shares_operation_notebook()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # protocol方法为此协议安装处理程序，此处用户关闭窗口的时间触发
        self.window.mainloop()
