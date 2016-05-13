import toga

def do_sync(widget):
    print('Sync', widget)

def build(app):
    container = toga.Container()
    button = toga.Button('Syncronise', on_press=do_sync)
    container.add(button)
    #container.constrain(button.TOP == container.TOP + 50)
    #container.constrain(button.LEADING == container.LEADING + 50)
    container.constrain(button.TRAILING + 50 == container.TRAILING)
    container.constrain(button.BOTTOM + 50 < container.BOTTOM)
    return container


if __name__=='__main__':
    app = toga.App('Simple file sync', 'org.anglicarets.filesync', startup=build)
    app.main_loop()
