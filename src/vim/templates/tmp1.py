#!/usr/bin/python

"""
    Created by: Ryan Moore
    Contact   : ryanmoore88@gmail.com
"""

import sys
import os
import argparse

def main(argv):
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--input', '-i',
            required=True,
            type=str,
            help='TODO')

    args = parser.parse_args(args=argv[1:])
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))
