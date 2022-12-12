#!/usr/bin/env python3

import os
import signal
import logging
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
        now = datetime.datetime.now()
        logging.info('Current time is {}.  Next check will run in {} seconds at {}'.format(now, self._period, now + datetime.timedelta(seconds=self._period)))

    def stop_timer(self) -> None:
        self._running = False
        self.timer.cancel()

    def exit_gracefully(self, *args) -> None:
        logging.error('Shutting down now.')
        self.stop_timer()
        self._done_lock.release()

    def _check_disks(self) -> None:
        logging.info('Running disk check now.')
        for disk in self._disks:
            logging.info('\tChecking {}'.format(disk))
        if self._running:
            self.run_timer()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill Velocity Monitor')
    parser.add_argument('-p', '--period', type=int, required=True, help='Monitoring period in seconds')
    parser.add_argument('disks', metavar='D', type=str, nargs='+', help='Paths to disks to be monitored')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')

    disks = [os.path.abspath(d) for d in args.disks]

    kill_mgr = KillManager()
    done_lock = threading.Lock()
    checker = DiskChecker(done_lock, args.period, disks)

    logging.info(f'Disk capacity will be checked every {args.period} seconds.')
    logging.info(f'Disks to be monitored: {disks}')

    checker.run_timer()
    done_lock.acquire()
