__author__ = '工具人'
import os
import tkinter as tk
from PIL import Image, ImageTk
from shares.share_server.get_quotation_photo_server import GetQuotationPhotoServer


class QuotationNotebookBuild:
    def __init__(self, root, logger, shares_name):
        self.root = root
        self.logger = logger
        self.shares_name = shares_name

    def quotation_note_build(self):
        GetQuotationPhotoServer(self.logger, self.shares_name).get_min_quotation_photo()
        parent_path = os.path.realpath(__file__).replace('\shar es\share_build\\toplevel_notebook\quotation_notebook_build.py', '')
        print(parent_path)
        image = Image.open(os.path.join(parent_path, '%s.jpg' % self.shares_name))  # 打开图片流
        x, y = image.size
        print(x, y)
        # image = image.resize((545, int(450*(y/x))+20), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        l1 = tk.Label(self.root, bg='white')
        l1.config(image=photo)
        l1.image = photo
        l1.pack()
