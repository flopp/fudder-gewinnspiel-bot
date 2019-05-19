#!/usr/bin/env python3

import argparse
from fudder import Fudder

def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-u', '--username', dest='username', metavar='USERNAME', type=str, required=True)
    args_parser.add_argument('-p', '--password', dest='password', metavar='PASSWORD', type=str, required=True)
    args_parser.add_argument('-d', '--data-dir', dest='data_dir', metavar='DIR', type=str, default='.data')
    args = args_parser.parse_args()

    f = Fudder(args.username, args.password, args.data_dir)
    f.get_new_gewinnspiele()

if __name__ == '__main__':
    main()
