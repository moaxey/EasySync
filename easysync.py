#!/usr/bin/env python
from tkinter import font
import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.menuBar = tk.Menu(self)
        self.subMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Help', menu=self.subMenu)
        self.subMenu.add_command(label='About', command=lambda *args: print(args))
        self.grid(padx=12, pady=12)
        self.wfs = tk.StringVar()
        self.sfs = tk.StringVar()
        self.active = tk.IntVar()
        self.wfs.set('Not selected')
        self.sfs.set('Not selected')
        self.active.set(0)
        self.createWidgets()

    def createWidgets(self):
        headfont = font.Font(family="Avenir Next", size=48, weight='bold')
        messagefont = font.Font(family="Avenir Next", size=18)
        labelfont = font.Font(family="Avenir Next", size=18, weight='bold')
        heading = tk.Label(
            self,
            text="EasySync",
            font=headfont,
            justify=tk.CENTER,
        ).grid(
            row=1,
            columnspan=3,
        )
        description = tk.Label(
            self,
            text="Sync your local working files to a second location.",
            font=messagefont,
            justify=tk.CENTER,
        ).grid(
            row=2,
            columnspan=3,
        )
        wflab =  tk.Label(
            self,
            text="Working files:",
            font=labelfont,
        ).grid(
            row=3,
            sticky=tk.E,
        )
        wfbut = tk.Button(
            self,
            text="Choose",
            padx=8,
            pady=4,
        ).grid(
            row=3,
            column=1,
            sticky=tk.W,
        )
        wfsel =  tk.Label(
            self,
            textvariable=self.wfs,
            font=messagefont,
            justify=tk.CENTER,
        ).grid(
            row=4,
            columnspan=3,
        )
        sflab =  tk.Label(
            self,
            text="Sync to:",
            font=labelfont,
        ).grid(
            row=5,
            sticky=tk.E,
        )
        sfbut = tk.Button(
            self,
            text="Choose",
            padx=8,
            pady=4,
        ).grid(
            row=5,
            column=1,
            sticky=tk.W,
        )
        sfsel =  tk.Label(
            self,
            textvariable=self.sfs,
            font=messagefont,
            justify=tk.CENTER,
        ).grid(
            row=6,
            columnspan=3,
        )
        sflab =  tk.Label(
            self,
            text="Activate:",
            font=labelfont,
        ).grid(
            row=7,
            sticky=tk.E,
        )
        active = tk.Checkbutton(
            self,
            text='Watch and sync',
            variable=self.active,
        ).grid(
            row=7,
            column=1,
            sticky=tk.W,
        )

"""
        self.quitButton = tk.Button(self, text='Quit',
            command=self.quit)
        self.quitButton.grid()

=============================

Easysync


Sync your local working files to a second location.

Working files: [ Select ]
filepath

Backup location:  [ Select ]
filepath


[ ] Watch and sync
Running / not running

[ View log ]

-------------------

[ Mirror ]

Syncs and deletes files from server that are not in your local working files

==============================




"""
app = Application()
app.master.title('EasySync')
app.mainloop()

