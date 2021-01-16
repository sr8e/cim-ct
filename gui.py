import tkinter as tk
import webbrowser

from tkinter import ttk
from ttkthemes import ThemedTk

from fileopen import FileOpenFrame
from converter import CimConverter, ConversionError


class Application(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(fill=tk.BOTH, expand=1)
        frame = ttk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.X, expand=1, anchor=tk.N)

        self.fileopener = FileOpenFrame(frame)
        self.fileopener.pack(side=tk.TOP, fill=tk.X, expand=1, padx=30, anchor=tk.N)

        frame_b = ttk.Frame(frame)
        frame_b.pack(side=tk.TOP, fill=tk.X, expand=1, padx=30, anchor=tk.N)

        ttk.Button(frame_b, text='変換', command=self.convert).pack(side=tk.RIGHT)

        frame_l = ttk.LabelFrame(self, text='コンソール', borderwidth=1, relief=tk.SOLID)
        frame_l.pack(side=tk.TOP, fill=tk.X, expand=1, padx=30, pady=20, anchor=tk.N)

        self.log = tk.Text(frame_l, height=8, state=tk.DISABLED, font=('Consolas', 10))
        self.log.pack(fill=tk.X, expand=1, padx=10, pady=10)

        bottom_bar = ttk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=1, anchor=tk.S)

        ttk.Label(bottom_bar, text='CIM Conversion Tool v1.0, by @sr_8e. See Details at ').pack(side=tk.LEFT)
        label_link = ttk.Label(bottom_bar, text='sr8e/cim-ct', foreground='#0000ff')
        label_link.bind('<Button-1>', lambda e: webbrowser.open_new('https://github.com/sr8e/cim-ct'))
        label_link.pack(side=tk.LEFT)
        ttk.Label(bottom_bar, text='.').pack(side=tk.LEFT)

    def convert(self, *args):
        self.log.configure(state=tk.NORMAL)
        is_to_png = self.fileopener.ctype.get() == 0
        is_single = self.fileopener.stype.get() == 0
        if is_single:
            src = self.fileopener.srcfilepath.get()
        else:
            src = self.fileopener.srcfolderpath.get()

        try:
            cc = CimConverter(is_to_png, is_single, src)

            if is_single:
                res = cc.execute()
                self.log.insert(tk.END, res + '\n')
            else:
                for res in cc.execute():
                    self.log.insert(tk.END, res + '\n')
        except ConversionError as ce:
            self.log.insert(tk.END, ce.message + '\n')

        self.log.see(tk.END)
        self.log.configure(state=tk.NORMAL)


root = ThemedTk(theme="arc")
root.geometry('800x600')
root.title('cim conversion tool')
# root.iconbitmap(settings.icon)

app = Application(root)
app.mainloop()
