#!/usr/bin/env python
from tkinter import font, ttk
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
        self.progress = tk.IntVar()
        self.action = tk.StringVar()
        self.wfs.set('Not selected')
        self.sfs.set('Not selected')
        self.action.set('No activity')
        self.active.set(0)
        self.createWidgets()

    def createWidgets(self):
        headfont = font.Font(family="Avenir Next", size=48, weight='bold')
        messagefont = font.Font(family="Avenir Next", size=18)
        labelfont = font.Font(family="Avenir Next", size=18, weight='bold')
        helpfont = font.Font(family="Avenir Next", size=12)
        rowcursor = 1
        heading = tk.Label(
            self,
            text="EasySync",
            font=headfont,
            justify=tk.CENTER,
        ).grid(
            row=rowcursor,
            columnspan=3,
        )
        rowcursor += 1
        description = tk.Label(
            self,
            text="Sync your local working files to a second location.",
            font=messagefont,
            justify=tk.CENTER,
        ).grid(
            row=rowcursor,
            columnspan=3,
        )
        rowcursor += 1
        sep = ttk.Separator(
            self,
            orient=tk.HORIZONTAL,
        ).grid(
            row=rowcursor,
            columnspan=3,
            sticky=tk.W+tk.E,
            pady=24,
        )
        rowcursor += 1
        wflab =  tk.Label(
            self,
            text="Working files:",
            font=labelfont,
        ).grid(
            row=rowcursor,
            sticky=tk.E,
        )
        wfbut = tk.Button(
            self,
            text="Choose",
            padx=8,
            pady=4,
            command=self.choose_working_folder,
        ).grid(
            row=rowcursor,
            column=1,
            sticky=tk.W,
        )
        rowcursor += 1
        wfsel =  tk.Label(
            self,
            textvariable=self.wfs,
            font=messagefont,
            justify=tk.CENTER,
        ).grid(
            row=rowcursor,
            columnspan=3,
        )
        rowcursor += 1
        sflab =  tk.Label(
            self,
            text="Sync to:",
            font=labelfont,
        ).grid(
            row=rowcursor,
            sticky=tk.E,
        )
        sfbut = tk.Button(
            self,
            text="Choose",
            padx=8,
            pady=4,
            command=self.choose_sync_folder,
        ).grid(
            row=rowcursor,
            column=1,
            sticky=tk.W,
        )
        rowcursor += 1
        sfsel =  tk.Label(
            self,
            textvariable=self.sfs,
            font=messagefont,
            justify=tk.CENTER,
        ).grid(
            row=rowcursor,
            columnspan=3,
        )
        rowcursor += 1
        sflab =  tk.Label(
            self,
            text="Activate:",
            font=labelfont,
        ).grid(
            row=rowcursor,
            sticky=tk.E,
        )
        active = tk.Checkbutton(
            self,
            text='Watch and sync',
            variable=self.active,
            command=self.toggle_activate,
        ).grid(
            row=rowcursor,
            column=1,
            sticky=tk.W,
        )
        rowcursor += 1
        actpb = ttk.Progressbar(
            self,
            orient=tk.HORIZONTAL,
            mode='indeterminate',
            variable=self.progress,
            length=200,
        ).grid(
            row=rowcursor,
            column=1,
            sticky=tk.W,
        )
        rowcursor += 1
        sflab =  tk.Label(
            self,
            textvariable=self.action,
            font=helpfont,
        ).grid(
            row=rowcursor,
            column=1,
            sticky=tk.W,
        )
        rowcursor += 1
        sep = ttk.Separator(
            self,
            orient=tk.HORIZONTAL,
        ).grid(
            row=rowcursor,
            columnspan=3,
            sticky=tk.W+tk.E,
            pady=24,
        )
        rowcursor += 1
        sflab =  tk.Label(
            self,
            text="Cleanup:",
            font=labelfont,
        ).grid(
            row=rowcursor,
            sticky=tk.E,
        )
        sfbut = tk.Button(
            self,
            text="Delete files",
            padx=8,
            pady=4,
            command=self.cleanup
        ).grid(
            row=rowcursor,
            column=1,
            sticky=tk.W,
        )
        rowcursor += 1
        sflab =  tk.Label(
            self,
            text="Delete 'Sync' files which are not in 'Working'",
            font=helpfont,
        ).grid(
            row=rowcursor,
            column=1,
            sticky=tk.W,
        )

    def choose_working_folder(self):
        print('Choose working')

    def choose_sync_folder(self):
        print('Choose sync')

    def toggle_activate(self):
        self.action.set('Waiting for changes')
        print('toggle activate')

    def cleanup(self):
        self.action.set('Cleaning up')
        print('cleanup')
        

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

