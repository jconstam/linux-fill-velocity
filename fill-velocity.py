#!/usr/bin/env python3

import signal
import logging
import argparse
import datetime
import threading
import subprocess

from influxdb import InfluxDBClient


class DBHandler:
    def __init__(self, ip_addr: str, port: int, username: str, password: str, db_name: str) -> None:
        logging.info('Connecting to InfluxDB at {}:{} with {}:******* using {}'.format(ip_addr, port, username, db_name))
        self._db_client = InfluxDBClient(ip_addr, port, username, password, db_name)

    def prepare_for_data(self):
        self._next_ts = datetime.datetime.utcnow().isoformat()
        self._next_data = []

    def add_data(self, drive_name: str, pct_full: float):
        self._next_data.append({'measurement': drive_name, 'time': self._next_ts, 'fields': {'pct_full': pct_full}})

    def write(self):
        assert self._next_data, 'No data has been added for writing'
        if not self._db_client.write_points(self._next_data):
            logging.warn('Could not write data to influxdb')


class DiskChecker:
    def __init__(self, period: int, drive_prefix: str, db: DBHandler) -> None:
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
        db.prepare_for_data()
        lines = output.split('\n')
        for line in lines:
            line_parts = line.split()
            if len(line_parts) == 6 and line_parts[0].startswith(self._drive_prefix):
                name = line_parts[0]
                total = int(line_parts[1])
                used = int(line_parts[2])
                pct_full = used / total
                logging.info('\t{}: {}/{} = {:.3f}%'.format(name, used, total, pct_full * 100))
                db.add_data(name, pct_full)
        db.write()
        if self._running:
            self.run_timer()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill Velocity Monitor')
    parser.add_argument('-p', '--period', type=int, required=True, help='Monitoring period in seconds')
    parser.add_argument('-d', '--drive_prefix', type=str, required=True, help='Prefix for drives to measure')
    parser.add_argument('-i', '--influxdb_ipaddr', type=str, required=True, help='IP Address for InfluxDB Instance')
    parser.add_argument('-t', '--influxdb_port', type=int, required=True, help='TCP Port for InfluxDB Instance')
    parser.add_argument('-u', '--influxdb_username', type=str, required=True, help='User Name for InfluxDB')
    parser.add_argument('-w', '--influxdb_password', type=str, required=True, help='Password for InfluxDB')
    parser.add_argument('-n', '--influxdb_databasename', type=str, required=True, help='Name of the Database in InfluxDB')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')

    logging.info(f'Disk capacity for drives starting with "{args.drive_prefix}" will be checked every {args.period} seconds.')

    db = DBHandler(args.influxdb_ipaddr, args.influxdb_port, args.influxdb_username, args.influxdb_password, args.influxdb_databasename)

    checker = DiskChecker(args.period, args.drive_prefix, db)
    checker.run_timer(True)
    checker.wait_for_done()
