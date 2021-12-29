# import gi
# from gi.repository import Notify
# from gi.repository import AppIndicator3
# from gi.repository import Gtk
# import os
# import subprocess
# import pickle

# from pathlib import Path


# class OpenVPN3ManagerApplet:
#     DIALOG_RETURN_CLOSE = -4
#     DIALOG_RETURN_CANCEL = 0
#     DIALOG_RETURN_SAVE = 1

#     def __init__(self):
#         self._build_applet()

#     def _build_applet(self):
#         """
#         Starts the building of the applet and menu items
#         """

#         self._applet = AppIndicator3.Indicator.new(
#             "system-lock-screen",
#             "dialog-password",
#             AppIndicator3.IndicatorCategory.APPLICATION_STATUS
#         )
#         self._applet.set_status(
#             AppIndicator3.IndicatorStatus.ACTIVE
#         )

#         # Create the applet menu
#         self._menu = Gtk.Menu()

#         self._applet.set_menu(self._menu)

#     def run(self):
#         Gtk.main()
#         return 0


# if __name__ == "__main__":
#     manager = OpenVPN3ManagerApplet()
#     manager.run()

# Create window
# gi.require_version("Gtk", "3.0")

# window = Gtk.Window(title="Hello World")
# window.show()
# window.connect("destroy", Gtk.main_quit)
# Gtk.main()


#!/usr/bin/env python3
import time
import threading
from gi.repository import Notify
from gi.repository import Gtk
from gi.repository import GLib
import signal
import os
from gi.repository import AppIndicator3
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')


CURRPATH = os.path.dirname(os.path.realpath(__file__))
ICON = os.path.join(CURRPATH, "tomato.png")
stop_threads = False
TITLE = 'Tomato Time'


class Indicator():
    def __init__(self):
        self.app = TITLE
        self.set_message('Start your productive time!')
        self.notifier = Notify.init(TITLE)

    def create_menu(self):
        menu = Gtk.Menu()

        menuitem_open = Gtk.MenuItem(label=TITLE)
        menuitem_open.set_sensitive(False)
        menu.append(menuitem_open)

        menu.append(Gtk.SeparatorMenuItem())

        item_1 = Gtk.MenuItem('Start!')
        item_1.connect('activate', self.init_countdown)

        # item_about.connect('activate', self.about)
        menu.append(item_1)
        # separator
        # menu_sep = Gtk.SeparatorMenuItem()
        # menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def init_countdown(self, widget):
        self.notify('Productive time has started!')
        global stop_threads
        stop_threads = True
        self.kill_thread_by_name('count')

        # the thread:
        stop_threads = False
        update = threading.Thread(target=self.countdown, name='count')
        # daemonize the thread to make the indicator stopable
        update.setDaemon(False)
        update.start()

    def kill_thread_by_name(self, name):
        threads = threading.enumerate()  # Threads list
        for thread in threads:
            if thread.name == name:
                thread.join()

    def set_message(self, message):
        self.indicator = AppIndicator3.Indicator.new(
            self.app, ICON,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label(message, self.app)

    # define the countdown func.
    def countdown(self):
        self.set_message('Have a nice productive time!')
        global stop_threads
        t = 1500
        while t >= 0:
            if(stop_threads):
                break
            time.sleep(1)
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            GLib.idle_add(
                self.indicator.set_label,
                timer, self.app,
                priority=GLib.PRIORITY_DEFAULT
            )
            t -= 1
        self.notify('Productive time finished!')

    def stop(self, source):
        global stop_threads
        stop_threads = True
        self.kill_thread_by_name('count')
        Gtk.main_quit()

    def notify(self, notice):
        self.notifier = Notify.Notification.new(
            TITLE, notice, ICON)
        self.notifier.show()


Indicator()
# this is where we call GObject.threads_init()
GLib.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
