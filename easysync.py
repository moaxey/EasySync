#!/usr/bin/env python
from __future__ import print_function, unicode_literals, absolute_import


import toga

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
        self.webview.url = 'http://google.com.au'


if __name__=='__main__':
    app = Swim('SyncSwim', 'org.anglicaretas.syncswim')
    app.main_loop()
