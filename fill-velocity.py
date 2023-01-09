#!/usr/bin/env python3

import signal
import logging
import argparse
import datetime
import threading
import subprocess


class DiskChecker:
    def __init__(self, period: int, drive_prefix: str) -> None:
        self._period = period
        self._drive_prefix = drive_prefix
        self._running = True
        self._done_lock = threading.Lock()
        self._done_lock.acquire()
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def run_timer(self, run_now: bool = False) -> None:
        run_period = 0.1 if run_now else self._period
        self.timer = threading.Timer(run_period, self._check_disks)
        self.timer.start()
        logging.info('Next check will run in {} seconds at {}'.format(run_period, datetime.datetime.now() + datetime.timedelta(seconds=run_period)))

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
        try:
            output = subprocess.check_output(['df']).decode()
        except subprocess.CalledProcessError as e:
            logging.error('Could not read drive information: {}'.format(e.args))
            return
        lines = output.split('\n')
        for line in lines:
            line_parts = line.split()
            if len(line_parts) == 6 and line_parts[0].startswith(self._drive_prefix):
                name = line_parts[0]
                total = int(line_parts[1])
                used = int(line_parts[2])
                logging.info('\t{}: {}/{} = {:.3f}%'.format(name, used, total, used / total * 100))
        if self._running:
            self.run_timer()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill Velocity Monitor')
    parser.add_argument('-p', '--period', type=int, required=True, help='Monitoring period in seconds')
    parser.add_argument('-d', '--drive_prefix', type=str, required=True, help='Prefix for drives to measure')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')

    logging.info(f'Disk capacity for drives starting with "{args.drive_prefix}" will be checked every {args.period} seconds.')

    checker = DiskChecker(args.period, args.drive_prefix)
    checker.run_timer(True)
    checker.wait_for_done()
