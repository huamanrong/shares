__author__ = '工具人'
import os
import time
import tkinter as tk
from PIL import Image, ImageTk
from shares.share_until.thread_until import ThreadUntil
from shares.share_server.get_quotation_photo_server import GetQuotationPhotoServer
import threading


class QuotationNotebookBuild:
    def __init__(self, root, logger, shares_name):
        self.root = root
        self.logger = logger
        self.shares_name = shares_name

    def quotation_note_build(self):
        self.photo_lable = tk.Label(self.root, bg='white')
        self.photo_lable.pack()
        thread = ThreadUntil()
        tid = thread.create_thread(self.refresh_photo)
        thread.thread_dict['quotation_notebook_build'] = tid

    def refresh_photo(self):
        GetQuotationPhotoServer(self.logger, self.shares_name).get_min_quotation_photo()
        while True:
            if not os.path.exists('%s.jpg' % self.shares_name):
                continue
            image = Image.open('%s.jpg' % self.shares_name)  # 打开图片流
            # x, y = image.size
            # image = image.resize((450, int(400*(y/x))+20), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.photo_lable.config(image=photo)
            self.photo_lable.image = photo
            print('refresh_photo')
            print('refresh_photo', threading.enumerate())
            time.sleep(3)
            GetQuotationPhotoServer(self.logger, self.shares_name).get_min_quotation_photo()


