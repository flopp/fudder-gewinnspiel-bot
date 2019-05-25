#!/usr/bin/env python3

import argparse
import sys
from fudder import Fudder

def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-u', '--username', dest='username', metavar='USERNAME', type=str)
    args_parser.add_argument('-p', '--password', dest='password', metavar='PASSWORD', type=str)
    args_parser.add_argument('-c', '--credentials', dest='credentials', metavar='FILE', type=str)
    args_parser.add_argument('-d', '--data-dir', dest='data_dir', metavar='DIR', type=str, default='.data')
    args = args_parser.parse_args()

    username = None
    password = None
    if args.credentials:
        with open(args.credentials) as f:
            for line in f:
                if username is None:
                    username = line.strip()
                elif password is None:
                    password = line.strip()
                else:
                    break
    if (username is None) or (password is None):
        if args.username and args.password:
            username = args.username
            password = args.password
    
    if (username is None) or (password is None):
        print('no username/password')
        sys.exit(1)

    f = Fudder(username, password, args.data_dir)
    f.get_new_gewinnspiele()

if __name__ == '__main__':
    main()
