#!/usr/bin/env python3

import os
import time
import signal
import argparse
import datetime
import threading


class KillManager:
    def __init__(self) -> None:
        self.running = True


class DiskChecker:
    def __init__(self, done_lock: threading.Lock, period: int, disks: list) -> None:
        self._period = period
        self._disks = disks
        self._running = True
        self._done_lock = done_lock
        self._done_lock.acquire()
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def run_timer(self) -> None:
        self.timer = threading.Timer(self._period, self._check_disks)
        self.timer.start()
        print('Setting timer to check disks in {} seconds at {}.'.format(self._period, datetime.datetime.now() + datetime.timedelta(seconds=self._period)))

    def stop_timer(self) -> None:
        self._running = False
        self.timer.cancel()

    def exit_gracefully(self, *args) -> None:
        print('Attempting to exit gracefully...')
        self.stop_timer()
        self._done_lock.release()

    def _check_disks(self) -> None:
        print('Running disk check at {}'.format(datetime.datetime.now()))
        for disk in self._disks:
            print('\tChecking {}'.format(disk))
        if self._running:
            self.run_timer()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill Velocity Monitor')
    parser.add_argument('-p', '--period', type=int, required=True, help='Monitoring period in seconds')
    parser.add_argument('disks', metavar='D', type=str, nargs='+', help='Paths to disks to be monitored')
    args = parser.parse_args()

    disks = [os.path.abspath(d) for d in args.disks]

    kill_mgr = KillManager()
    done_lock = threading.Lock()
    checker = DiskChecker(done_lock, args.period, disks)

    print(f'Disk capacity will be checked every {args.period} hours')
    print(f'Disks to be monitored: {disks}')

    checker.run_timer()
    done_lock.acquire()
