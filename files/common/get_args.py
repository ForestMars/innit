#!/usr/bin/python3
# get_args.py - Arg parger module template
"""
    -h  show this help text
    -o  optional parameter
    -v  verboe mode
"""

import argparse

DESCRIPTION=''


def get_args():

    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog = """ EPILOG """
        )

    parser.add_argument('-o', '--option_one', action="store", dest='one', default=None, help='this is option one.', metavar='')

    args = parser.parse_args()

    return args

# ???
if __name__ == '__main__':
    get_args()
