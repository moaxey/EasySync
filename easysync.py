#!/usr/bin/env python
from __future__ import print_function, unicode_literals, absolute_import
import time
import toga
from multiprocessing import Process
from guts import runner


class Swim(toga.App):

    def startup(self):
        container = toga.Container()
        self.webview = toga.WebView()
        container.add(self.webview)
        container.constrain(self.webview.TOP == container.TOP)
        container.constrain(self.webview.BOTTOM == container.BOTTOM)
        container.constrain(self.webview.RIGHT == container.RIGHT)
        container.constrain(self.webview.LEFT == container.LEFT)
        self.main_window.content = container
        self.webview.url = 'http://127.0.0.1:5000/'

    def load_page(self, widget=None):
        self.webview.url = 'http://127.0.0.1:5000/'


if __name__=='__main__':
    app = Swim('SyncSwim', 'org.anglicaretas.syncswim')
    pp = Process(target=runner)
    pp.start()
    time.sleep(5)
    app.main_loop()
    pp.terminate()
    pp.join()


