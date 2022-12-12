#!/usr/bin/env python3

import os
import signal
import logging
import argparse
import datetime
import threading


class DiskChecker:
    def __init__(self, period: int, disks: list) -> None:
        self._period = period
        self._disks = disks
        self._running = True
        self._done_lock = threading.Lock()
        self._done_lock.acquire()
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def run_timer(self) -> None:
        self.timer = threading.Timer(self._period, self._check_disks)
        self.timer.start()
        logging.info('Next check will run in {} seconds at {}'.format(self._period, datetime.datetime.now() + datetime.timedelta(seconds=self._period)))

    def stop_timer(self) -> None:
        self._running = False
        self.timer.cancel()

    def wait_for_done(self) -> None:
        self._done_lock.acquire()

    def _exit_gracefully(self, *args) -> None:
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

    logging.info(f'Disk capacity will be checked every {args.period} seconds.')
    logging.info(f'Disks to be monitored: {disks}')

    checker = DiskChecker(args.period, disks)

    checker.run_timer()
    checker.wait_for_done()
