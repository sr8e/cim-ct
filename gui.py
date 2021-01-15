import tkinter as tk

from tkinter import ttk
from ttkthemes import ThemedTk

from fileopen import FileOpenFrame
from converter import CimConverter, ConversionError


class Application(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(fill=tk.BOTH, expand=1)
        frame = ttk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.fileopener = FileOpenFrame(frame)

        self.fileopener.pack(side=tk.TOP, fill=tk.X, expand=1, padx=30)

        frame_b = ttk.Frame(frame)
        frame_b.pack(side=tk.TOP, fill=tk.X, expand=1, padx=30)

        ttk.Button(frame_b, text='変換', command=self.convert).pack(side=tk.RIGHT)

        frame_l = ttk.LabelFrame(self, text='コンソール', borderwidth=1, relief=tk.SOLID)
        frame_l.pack(side=tk.BOTTOM, fill=tk.X, expand=1, padx=30, pady=20)

        self.log = tk.Text(frame_l, height=8, state=tk.DISABLED, font=('Consolas', 10))
        self.log.pack(fill=tk.X, expand=1, padx=10, pady=10)

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
