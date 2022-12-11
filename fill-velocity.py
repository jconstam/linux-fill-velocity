#!/usr/bin/env python3

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill Velocity Monitor')
    parser.add_argument('-p', '--port', type=int, default=8080, help='TCP port for Web UI')
    parser.add_argument('disks', metavar='D', type=str, nargs='+', help='Paths to disks to be monitored')
    args = parser.parse_args()

    print('Using TCP port {}'.format(args.port))
    print('Disks to be monitored: {}'.format(args.disks))
