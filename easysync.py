#!/usr/bin/env python
from tkinter import font, ttk, filedialog
import tkinter as tk
from appdirs import AppDirs
import configparser
import os

class AppConfig():

    def __init__(self):
        self.dirs = None
        self.app_title = ''
        self.config = None

    def config_setup(self, app_title):
        self.dirs = AppDirs(app_title, "Author")
        if not os.path.exists(self.dirs.user_config_dir):
            os.makedirs(self.dirs.user_config_dir)
        self.app_title = app_title
        self.read_config()
        self.configure_gui()

    def get_config_path(self):
        return os.path.join(
            self.dirs.user_config_dir,
            '{}.conf'.format(self.app_title)
        )

    def get_default_config(self):
        return {'section': {'key': 'value'}}

    def read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(
            self.get_config_path()
        )
        dc = self.get_default_config()
        anychange = False
        for section, default_values  in dc.items():
            if section not in self.config.sections():
                self.config[section] = default_values
                anychange = True
        if anychange:
            self.write_config()

    def write_config(self):
        with open(
                self.get_config_path(), 'w'
        ) as cf:
            self.config.write(cf)

    def purge_config(self):
        os.unlink(self.get_config_path())

    def configure_gui(self):
        pass

class Application(tk.Frame, AppConfig):

    def __init__(self, master=None):
        super().__init__()
        tk.Frame.__init__(self, master)
        self.menuBar = tk.Menu(self)
        self.subMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(
            label='Help', menu=self.subMenu
        )
        self.subMenu.add_command(
            label='About', command=lambda *args: print(args)
        )
        self.grid(padx=12, pady=12)
        self.wfs_dir = tk.StringVar()
        self.sfs_dir = tk.StringVar()
        self.active = tk.IntVar()
        self.progress = tk.IntVar()
        self.action = tk.StringVar()
        self.action.set('No activity')
        self.create_widgets()

    def get_default_config(self):
        return {
            'state': {
                'wfs_dir': '',
                'sfs_dir': '',
                'active': False,
            }
        }

    def configure_gui(self):
        print('zzz', self.config)
        self.wfs_dir.set(self.config['state']['wfs_dir'])
        self.sfs_dir.set(self.config['state']['sfs_dir'])
        self.active.set(self.config.getboolean('state', 'active'))

    def create_widgets(self):
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
            textvariable=self.wfs_dir,
            font=helpfont,
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
            textvariable=self.sfs_dir,
            font=helpfont,
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
        # read current setting for default or home
        self.wfs_dir.set(
            filedialog.askdirectory(
            )
        )

    def choose_sync_folder(self):
        print('Choose sync')
        # read current setting for default or home
        self.sfs_dir.set(filedialog.askdirectory())

    def toggle_activate(self):
        self.action.set('Waiting for changes')
        ## turn on
        # deactivate ui elements
        # start macfsevents observer
        # set hook to sync from working (self.do_sync)
        ## turn off
        # stop macfsevents observer
        # wait for any dirsync to finish
        # activate ui elements
        print('toggle activate')

    def cleanup(self):
        self.action.set('Cleaning up')
        # sync and purge from working
        self.do_sync(purge=True)
        print('cleanup')

    def do_sync(self, **options):
        sync(
            self.wfs_dir.get(),
            self.sfs_dir.get(),
            'sync',
            logger=my_logger,
            **options
        )


if __name__=='__main__':
    app = Application()
    app.master.title('EasySync')
    app.config_setup('EasySync')
    app.mainloop()

