import tkinter as tk
import os
import sys

from tkinter import ttk
from tkinter import filedialog


class FileOpenFrame(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.ctype = tk.IntVar()  # conversion type: 0 for cim->png, 1 for png->cim

        frame_0 = ttk.LabelFrame(self, text='変換タイプ', borderwidth=1, relief=tk.SOLID)
        frame_0.pack(side=tk.TOP, fill=tk.X, expand=1, pady=15)

        radio_c0 = ttk.Radiobutton(frame_0, text='.cim -> .png', value=0, variable=self.ctype)
        radio_c1 = ttk.Radiobutton(frame_0, text='.png -> .cim', value=1, variable=self.ctype)

        radio_c0.pack(side=tk.LEFT, padx=15, pady=5)
        radio_c1.pack(side=tk.LEFT, pady=5)

        self.stype = tk.IntVar()  # file selection type: 0 for folder, 1 for file(s)

        frame_1 = ttk.LabelFrame(self, text='変換元ファイル・フォルダ選択', borderwidth=1, relief=tk.SOLID)
        frame_in_1 = ttk.Frame(frame_1)
        frame_in_2 = ttk.Frame(frame_1)

        frame_1.pack(side=tk.TOP, fill=tk.X, expand=1, pady=15)
        frame_in_2.pack(side=tk.TOP, fill=tk.X, expand=1, padx=15, pady=5)
        frame_in_1.pack(side=tk.TOP, fill=tk.X, expand=1, padx=15, pady=5)

        ttk.Radiobutton(frame_in_1, text='フォルダ選択', value=1, variable=self.stype).pack(side=tk.LEFT)
        ttk.Radiobutton(frame_in_2, text='ファイル選択', value=0, variable=self.stype).pack(side=tk.LEFT)

        self.srcfolderpath = tk.StringVar()
        self.srcfilepath = tk.StringVar()

        ttk.Entry(frame_in_1, textvariable=self.srcfolderpath).pack(side=tk.LEFT, fill=tk.X, expand=1)
        ttk.Entry(frame_in_2, textvariable=self.srcfilepath).pack(side=tk.LEFT, fill=tk.X, expand=1)

        ttk.Button(frame_in_1, text='開く...', command=self.select_folder).pack(side=tk.LEFT)
        ttk.Button(frame_in_2, text='開く...', command=self.select_file).pack(side=tk.LEFT)

        frame_2 = ttk.LabelFrame(self, text='保存先フォルダ指定', borderwidth=1, relief=tk.SOLID)
        frame_in_3 = ttk.Frame(frame_2)
        frame_in_4 = ttk.Frame(frame_2)

        frame_2.pack(side=tk.TOP, fill=tk.X, expand=1, pady=15)
        frame_in_3.pack(side=tk.TOP, fill=tk.X, expand=1, padx=15, pady=5)
        frame_in_4.pack(side=tk.TOP, fill=tk.X, expand=1, padx=15, pady=5)

        self.changedst = tk.IntVar()
        self.dstfolderpath = tk.StringVar()
        self.allow_mkdir = tk.IntVar()

        ttk.Checkbutton(frame_in_3, text='保存先フォルダを指定する', onvalue=1, offvalue=0, variable=self.changedst).pack(side=tk.LEFT)

        ttk.Entry(frame_in_3, textvariable=self.dstfolderpath).pack(side=tk.LEFT, fill=tk.X, expand=1)
        ttk.Button(frame_in_3, text='開く...', command=self.select_dstfolder).pack(side=tk.LEFT)

        ttk.Checkbutton(frame_in_4, text='フォルダが存在しない場合、新規作成する', onvalue=1, offvalue=0, variable=self.allow_mkdir).pack(side=tk.LEFT)

    def select_file(self, *args):
        types = [[('cimファイル', '*.cim')], [('pngファイル', '*.png')]]
        init_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.srcfilepath.set(filedialog.askopenfilename(filetypes=types[self.ctype.get()], initialdir=init_dir))

    def select_folder(self, *args):
        init_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.srcfolderpath.set(filedialog.askdirectory(initialdir=init_dir))

    def select_dstfolder(self, *args):
        init_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.dstfolderpath.set(filedialog.askdirectory(initialdir=init_dir))
