import time
import threading
import re
from pingerlib.run import run, run_nowait, append_ping_log
from pingerlib.config import config


def disconnect_action():
    run_nowait('nmcli con down VPN; nmcli con up VPN &', shell=True)


class Monitor(threading.Thread):
    def __init__(self):
        self.data_lock = threading.Lock()
        self.rtt = -1
        self.cycle = 0
        self.bad_cycle = 0
        self.good_cycle = 0
        self.stopping = False
        threading.Thread.__init__(self)

    def StopThread(self):
        self.stopping = True

    def getRtt(self):
        with self.data_lock:
            return self.rtt

    def setRtt(self, rtt):
        with self.data_lock:
            self.rtt = rtt

    def getStartTime(self):
        with self.data_lock:
            return self.start_time

    def setStartTime(self, start_time):
        with self.data_lock:
            self.start_time = start_time

    def getCycle(self):
        with self.data_lock:
            return self.cycle

    def setCycle(self, cycle):
        with self.data_lock:
            self.cycle = cycle

    def getBadCycle(self):
        with self.data_lock:
            return self.bad_cycle

    def setBadCycle(self, cycle):
        with self.data_lock:
            self.bad_cycle = cycle

    def getGoodCycle(self):
        with self.data_lock:
            return self.good_cycle

    def setGoodCycle(self, cycle):
        with self.data_lock:
            self.good_cycle = cycle

    def run(self):
        while True:
            with self.data_lock:
                if self.stopping:
                    return
            start_time = time.time()
            self.setStartTime(start_time)
            self.setRtt(self.ping())
            self.setStartTime(0)
            self.setCycle(self.getCycle() + 1)
            pause = config['PING_TIMEOUT'] - (time.time() - start_time)
            if pause > 0:
                time.sleep(pause)

    def ping(self):
        command = ['/bin/ping', '-c1', '-W{}'.format(config['PING_TIMEOUT']), config['HOST_TO_PING']]
        res = run(command, shell=False)
        match = re.search('time=([0-9.]+) ms', res)
        bad_cycle = self.getBadCycle()
        good_cycle = self.getGoodCycle()
        cycle = self.getCycle()
        if match:
            rtt = match.group(1)
            self.setGoodCycle(good_cycle + 1)
            self.setBadCycle(0)
            if not cycle or bad_cycle > config['MAX_ALLOWED_TIMEOUTS_COUNT']:
                append_ping_log(rtt)
            return float(rtt)
        else:
            self.setBadCycle(bad_cycle + 1)
            if bad_cycle == config['MAX_ALLOWED_TIMEOUTS_COUNT']:
                self.setGoodCycle(0)
                append_ping_log('Stable ping timeout')
                disconnect_action()
            return -1
