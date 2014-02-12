#!/usr/bin/env python

from __future__ import print_function

# Metadata
__version__ = '2.2.5'
last_updated = 'Mar-02-2012'

# Standard Library
import argparse
import resource

def check_mem_usage():

    pagesize = resource.getpagesize()


def nccombine(**args):
    # TODO: Replace "args" with the actual arguments
    
    pass


def nccombine_parse():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-v', action='store_true', dest='verbose')
    parser.add_argument('-M', action='store_true', dest='memstats')
    parser.add_argument('-f', action='store_true', dest='force')
    parser.add_argument('-a', action='store_true', dest='append')
    parser.add_argument('-r', action='store_true', dest='remove')
    parser.add_argument('-n', action='store', dest='initial_extension')
    parser.add_argument('-k', action='store', dest='blocking_factor')
    parser.add_argument('-e', action='store', dest='final_extension')
    parser.add_argument('-h', action='store', dest='byte_padding')
    parser.add_argument('-64', action='store_true', dest='use_nc_64offset')
    parser.add_argument('-n4', action='store_true', dest='use_nc_classic')
    parser.add_argument('-m', action='store_true', dest='missing_value')
    parser.add_argument('-x', action='store_true', dest='mem_estimate')

    parser.add_argument('-V', '--version', action='version',
                        version='mppnccombine version: {}'.format(__version__))

    args = parser.parse_args()
    print(args)

    return vars(args)


if __name__ == '__main__':
    args = nccombine_parse()
    nccombine(**args)
