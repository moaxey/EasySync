#!/usr/bin/env python

from tkinter import font, ttk, filedialog
import tkinter as tk
from appdirs import AppDirs
import configparser
import os
import time
import logging
from fsevents import Observer, Stream
from dirsync import sync

DEBUG=True
def debug(*args):
    if DEBUG:
        print(args)


class AppConfig():

    def __init__(self):
        self.dirs = None
        self.app_title = ''
        self.config = None

    def config_setup(self, app_title):
        self.dirs = AppDirs(app_title, "Author")
        if not os.path.exists(self.dirs.user_config_dir):
            os.makedirs(self.dirs.user_config_dir)
        if not os.path.exists(self.dirs.user_log_dir):
            os.makedirs(self.dirs.user_log_dir)
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
        top = self.winfo_toplevel()
        top.protocol("WM_DELETE_WINDOW", self.stop_observer)
        top.createcommand("tk::mac::Quit", self.stop_observer)
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar
        self.grid(padx=12, pady=12)
        self.wfs_dir = tk.StringVar()
        self.sfs_dir = tk.StringVar()
        self.active = tk.IntVar()
        self.progress = tk.IntVar()
        self.actions = []
        self.action = tk.StringVar()
        self.action_id = None
        self.activate_id = None
        self.ticker_id = None
        self.next_status_id = None
        self.observer = None
        self.stream = None
        self.app_icon = None
        self.app_icons = [
            tk.PhotoImage(file='icon/icon_{}.gif'.format(n))
            for n in range(1,5)
        ]
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
        self.wfs_dir.set(self.config['state']['wfs_dir'])
        self.sfs_dir.set(self.config['state']['sfs_dir'])
        self.active.set(int(self.config.getboolean('state', 'active')))
        self.toggle_activate()

    def tick_app_icon(self):
        debug('tick') #, self.app_icons)
        self.app_icons.insert(0, self.app_icons.pop())
        self.app_icon.configure(image=self.app_icons[0])

    def ticking(self):
        # prevent ticking loops if it is triggered multiple times in succession
        self.stop_ticking()
        self.tick_app_icon()
        self.ticker_id = self.after(100, self.ticking)

    def stop_ticking(self):
        if self.ticker_id is not None:
            self.after_cancel(self.ticker_id)
            self.ticker_id = None

    def create_widgets(self):
        headfont = font.Font(family="Avenir Next", size=54)
        messagefont = font.Font(family="Avenir Next", size=18)
        labelfont = font.Font(family="Avenir Next", size=18, weight='bold')
        helpfont = font.Font(family="Avenir Next", size=12)
        rowcursor = 1
        self.app_icon = tk.Label(
            self,
            image=self.app_icons[0],
        )
        self.app_icon.grid(
            row=rowcursor,
            column=0,
            sticky=tk.E,
        )
        heading = tk.Label(
            self,
            text="EasySync",
            font=headfont,
            justify=tk.LEFT,
        ).grid(
            row=rowcursor,
            column=1,
            columnspan=2,
            sticky=tk.W,
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
        self.wfbut = tk.Button(
            self,
            text="Choose",
            padx=8,
            pady=4,
            command=self.choose_working_folder,
        )
        self.wfbut.grid(
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
        self.sfbut = tk.Button(
            self,
            text="Choose",
            padx=8,
            pady=4,
            command=self.choose_sync_folder,
        )
        self.sfbut.grid(
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
            text='Watch working and copy to sync',
            variable=self.active,
            command=self.toggle_activate,
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
        self.purgebut = tk.Button(
            self,
            text="Delete files",
            padx=8,
            pady=4,
            command=self.cleanup
        )
        self.purgebut.grid(
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

    def choose_folder(self, configkey, variable):
        ov = variable.get()
        cwd = self.config['state'][configkey]
        if cwd == '':
            cwd = os.path.expanduser('~')
        selected = filedialog.askdirectory(
            initialdir=cwd
        )
        selected = ov if selected == '' else selected
        variable.set(selected)
        self.config['state'][configkey] = variable.get()
        self.write_config()

    def choose_working_folder(self):
        debug('Choose working')
        self.choose_folder('wfs_dir', self.wfs_dir)

    def choose_sync_folder(self):
        debug('Choose sync')
        self.choose_folder('sfs_dir', self.sfs_dir)

    def pad(self, string):
        return '{0: <43}'.format(string)

    def dirs_okay(self):
        # combined with reactivate, this allows sync to pause and continue if
        # either directory is absent (e.g. unmounted)
        wfs = self.wfs_dir.get()
        sfs = self.sfs_dir.get()
        wfsx = os.path.isdir(wfs)
        sfsx = os.path.isdir(sfs)
        if wfs == sfs or not wfsx or not sfsx:
            self.active.set(0)
            if wfs == sfs:
                self.action.set(
                    self.pad('Working and sync files are the same folder')
                )
            elif not wfsx or not sfsx:
                if not wfsx:
                    self.action.set(
                        self.pad('Working files folder does not exist')
                    )
                elif not sfsx:
                    self.action.set(
                        self.pad('Sync files folder does not exist')
                    )
            self.update_idletasks()
            return False
        else:
             return True

    def reactivate(self):
        self.activate_id = None
        self.active.set(1)
        self.toggle_activate()

    def toggle_activate(self):
        become_active = self.active.get()
        if self.activate_id is not None and become_active:
            # while failing to auto-activate allow user to deactivate
            # without changing stored preferences
            debug('cancelling timed activation')
            self.after_cancel(self.activate_id)
            self.activate_id = None
            self.wfbut['state'] = tk.NORMAL
            self.sfbut['state'] = tk.NORMAL
            self.purgebut['state'] = tk.NORMAL
            self.active.set(0)
            return
        debug('toggle activate', become_active)
        self.tick_app_icon()
        if become_active:
            ## turn on
            self.wfbut['state'] = tk.DISABLED
            self.sfbut['state'] = tk.DISABLED
            self.purgebut['state'] = tk.DISABLED
            self.queue_status('Looking for directories')
            self.update_idletasks()
            wfs = self.wfs_dir.get()
            if not self.dirs_okay():
                if self.activate_id is None:
                    self.activate_id = self.after(400, self.reactivate)
                return
            self.update_idletasks()
            self.do_sync()
            if self.observer is None:
                self.stream = Stream(self.do_sync, wfs)
                self.observer = Observer()
                self.observer.schedule(self.stream)
                self.observer.start()
        else:
            self.action.set(self.pad('Not active'))
            self.update_idletasks()
            ## turn off
            if self.observer:
                self.observer.unschedule(self.stream)
                self.observer.stop()
                self.observer = None
            self.wfbut['state'] = tk.NORMAL
            self.sfbut['state'] = tk.NORMAL
            self.purgebut['state'] = tk.NORMAL
        self.config['state']['active'] = str(become_active)
        self.write_config()

    def cleanup(self):
        debug('cleanup')
        thisaction = 'Cleaning up'
        self.action.set(self.pad(thisaction))
        self.update_idletasks()
        # sync and purge files not in working
        self.do_sync(purge=True, verbose=True)
        self.queue_status(thisaction)

    def stop_observer(self):
        debug('stop observer')
        if self.observer:
            self.observer.unschedule(self.stream)
            self.observer.stop()
            self.observer = None
        debug('stop actions')
        if self.action_id is not None:
            self.after_cancel(self.action_id)
        if self.activate_id is not None:
            self.after_cancel(self.activate_id)
        if self.ticker_id is not None:
            self.after_cancel(self.ticker_id)
        debug('quitting')
        self.quit()

    def do_sync(self, *args, **options):
        debug('do sync', args, options)
        if not self.dirs_okay():
            if self.activate_id is None:
                self.activate_id = self.after(400, self.reactivate)
            return
        if 'exclude' not in options.keys():
            # exclude hidden files, lock files, backup files
            options['exclude'] = [
                ".*\.DS_Store",
                ".+/\.[\w \.]+$",
                ".+/~.+\.idlk$",
                ".+/#.+$",
                ".+/.+~$",
            ]
        self.ticking()
        self.action.set(self.pad('Syncing'))
        self.update_idletasks()
        logfile = os.path.join(
            self.dirs.user_log_dir,
            '{}.log'.format(self.__class__.__name__)
        )
        logging.basicConfig(filename=logfile, level=logging.DEBUG)
        files = sync(
            self.wfs_dir.get(),
            self.sfs_dir.get(),
            'sync',
            logger=logging,
            **options
        )
        self.stop_ticking()
        self.queue_status('Copied {} files'.format(len(files)))

    def watching_status(self):
        # have a proper test here for thread alive
        if self.observer is None:
            self.action.set(self.pad('Not active'))
        else:
            self.action.set(self.pad('Watching for changes'))
        self.update_idletasks()
        self.next_status_id = None

    def next_status(self):
        action, duration = self.actions.pop(0)
        self.action.set(self.pad(action))
        self.update_idletasks()
        if len(self.actions) > 0:
            self.next_status_id = self.after(duration, self.next_status)
        else:
            self.next_status_id = self.after(duration, self.watching_status)

    def queue_status(self, action, duration=2000):
        # add to queue and call next_status
        self.actions.append((action, duration))
        if self.next_status_id is None:
            self.next_status()


if __name__=='__main__':
    app = Application()
    app.master.title('EasySync')
    app.config_setup('EasySync')
    app.mainloop()

