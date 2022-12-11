#!/usr/bin/env python3

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill Velocity Monitor')
    parser.add_argument('disks', metavar='D', type=str, nargs='+', help='Paths to disks to be monitored')
    args = parser.parse_args()

    print('Disks to be monitored: {}'.format(args.disks))
