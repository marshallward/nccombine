#!/usr/bin/env python

from __future__ import print_function


# Standard Library
import argparse

def nccombine(args):
    pass


def nccombine_parse():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-v', action='store_true')  # verbose
    parser.add_argument('-V', action='store_true')  # version
    parser.add_argument('-M', action='store_true')  # memory usage
    parser.add_argument('-f', action='store_true')  # force
    parser.add_argument('-a', action='store_true')  # append
    parser.add_argument('-r', action='store_true')  # remove old files
    parser.add_argument('-n')   # input extension (####)
    parser.add_argument('-k')   # blocking (???)
    parser.add_argument('-e')   # end extension
    parser.add_argument('-h')   # header padding
    parser.add_argument('-64', action='store_true') # 64-bit offset format
    parser.add_argument('-n4', action='store_true') # classic NETCDF format
    parser.add_argument('-m', action='store_true')  # Initialize output with `missing_value`
    parser.add_argument('-x', action='store_true')  # Estimate peak memory

    args = parser.parse_args()

    return args
    


if __name__ == '__main__':
    args = nccombine_parse()
    nccombine()
