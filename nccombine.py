#!/usr/bin/env python

from __future__ import print_function

# Metadata (spoofing the C program)
__version__ = '2.2.5'
last_updated = 'Mar-02-2012'

# Standard Library
import argparse
import os
import resource
import sys

# Extensions
import netCDF4 as nc

# Macros
MAX_BF = 100

def check_mem_usage():

    pagesize = resource.getpagesize()


def nccombine(verbose, print_mem_usage, force, append_nc, remove_input,
              n_start, bf, n_end, header_pad, use_nc3_64offset,
              use_nc4_classic, missing, mem_dry_run, output_fname,
              input_fnames):

    # Set NetCDF output type
    assert not (use_nc3_64offset and use_nc4_classic)

    if use_nc3_64offset:
        format = 'NETCDF3_64BIT'
    elif use_nc4_classic:
        format = 'NETCDF4_CLASSIC'
    else:
        format = 'NETCDF3_CLASSIC'

    
    if not append_nc:
        if os.path.isfile(output_fname):
            print('mppnccombine: error: output file seems to exist already!')
            return 1

    # Clean exit
    return 0


#---
def nccombine_parse():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-v', action='count', dest='verbose')
    parser.add_argument('-M', action='store_true', dest='print_mem_usage')
    parser.add_argument('-f', action='store_true', dest='force')
    parser.add_argument('-a', action='store_true', dest='append_nc')
    parser.add_argument('-r', action='store_true', dest='remove_input')
    parser.add_argument('-n', action='store', dest='n_start')
    parser.add_argument('-k', action='store', dest='bf')
    parser.add_argument('-e', action='store', dest='n_end')
    parser.add_argument('-h', action='store', dest='header_pad')
    parser.add_argument('-64', action='store_true', dest='use_nc3_64offset')
    parser.add_argument('-n4', action='store_true', dest='use_nc4_classic')
    parser.add_argument('-m', action='store_true', dest='missing')
    parser.add_argument('-x', action='store_true', dest='mem_dry_run')

    parser.add_argument('-V', '--version', action='version',
                        version='mppnccombine version: {}'.format(__version__))

    parser.add_argument('output_fname', metavar='output.nc')
    parser.add_argument('input_fnames', metavar='input', nargs='*')

    args = parser.parse_args()

    # Process input arguments
    args.n_start = int(args.n_start) if args.n_start else 0
    args.bf = int(args.bf) if args.bf else 1
    args.n_end = int(args.n_end) if args.n_end else -1
    args.header_pad = int(args.header_pad) if args.header_pad else 16384

    # Parse n_start and n_end a bit better
    # Specifically manage >4 character length
    # TODO
    
    if args.mem_dry_run:
        if args.bf != 1:
            print('-x is set, so blocking factor will be set to 1. The -k '
                  'option will be ignored.', file=sys.stderr)
            args.bf = 1
            if verbose:
                print('This run will estimate peak memory resident size. No '
                      'output file will be created.')

    if not args.mem_dry_run and args.bf > MAX_BF:
        print('nccombine: warning: k is set too high. Choosing a more sane '
              'value of {}.'.format(MAX_BF), file=sys.stderr)
        args.bf = MAX_BF

    if args.verbose == 3:
        print(args)
    return vars(args)


if __name__ == '__main__':
    args = nccombine_parse()
    rc = nccombine(**args)
    sys.exit(rc)
