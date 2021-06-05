import os
import time
from gi import require_version
from gi.repository import Gtk
from gi.repository.GLib import timeout_add, source_remove, idle_add, unix_signal_add, PRIORITY_HIGH
require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appIndicator

from pingerlib.monitor import Monitor
from pingerlib.run import run
from pingerlib.config import config


class TaskBarIcon():
    def __init__(self):
        self.cur_icon = ''
        self.ind = appIndicator.Indicator.new(
            "Pinger",
            os.path.abspath("img/circle-lightgray.png"),
            appIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appIndicator.IndicatorStatus.ACTIVE)
        self.create_menu()
        self.ind.set_menu(self.menu)

        timeout_add(config['GUI_MS_BETWEEN_REDRAWS'], self.update)
        self.gui_cycle = 0
        self.monitor = Monitor()
        self.monitor.start()

    def update(self):
        self.gui_cycle += 1
        self.update_icon()
        return True

    def update_icon(self):
        start_time = self.monitor.getStartTime()
        delta = (time.time() - start_time - 0.02) * 1000 if start_time else 0
        rtt = self.monitor.getRtt()
        cycle = self.monitor.getCycle()
        good_cycle = self.monitor.getGoodCycle()

        if rtt == -1:
            self.set_icon('red', cycle, good_cycle)
        elif rtt < config['MAX_BLUE_RTT'] and delta < config['MAX_BLUE_RTT']:
            self.set_icon('blue', cycle, good_cycle)
        elif rtt < config['MAX_GREEN_RTT'] and delta < config['MAX_GREEN_RTT']:
            self.set_icon('green', cycle, good_cycle)
        elif rtt < config['MAX_YELLOW_RTT'] and delta < config['MAX_YELLOW_RTT']:
            self.set_icon('yellow', cycle, good_cycle)
        else:
            self.set_icon('orange', cycle, good_cycle)


    def set_icon(self, path, cycle, good_cycle):
        full_path = 'img/circle-' + path
        if cycle % 2:
            full_path += '-dot'
            if good_cycle < config['RECOVERY_PINGS_COUNT']:
                full_path += '-white'
            else:
                full_path += '-black'
        full_path += '.png'
        if self.cur_icon == full_path:
            return
        self.cur_icon = os.path.abspath(full_path)

        self.ind.set_icon_full(self.cur_icon, '')

    def create_menu(self):
        self.menu = Gtk.Menu()

        self.menu.logs = Gtk.MenuItem(label='Logs')
        self.menu.logs.connect("activate", self.on_logs)
        self.menu.append(self.menu.logs)

        self.menu.append(Gtk.SeparatorMenuItem.new())

        self.menu.exit = Gtk.MenuItem(label='Exit Pinger')
        self.menu.exit.connect("activate", self.on_exit)
        self.menu.append(self.menu.exit)

        self.menu.show_all()

    def on_logs(self, widget):
        print(run('gnome-terminal -x bash -c "less logs/ping.log"', shell=True))

    def on_exit(self, widget):
        self.exit()

    def exit(self):
        self.monitor.StopThread()
        Gtk.main_quit()


