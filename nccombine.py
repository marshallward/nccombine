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

usage_message = """mppnccombine {} - (writtern by Hans.Vahlenkamp)

Usage:  mppnccombine [-v] [-V] [-M] [-a] [-r] [-n #] [-k #] [-e #] [-h #] [-64] [-n4] [-m]
                     output.nc [input ...]

  -v    Print some progress information.
  -V    Print version information.
  -M    Print memory usage statistics.
  -f    Force combine to happen even if input files are missing.
  -a    Append to an existing netCDF file (not heavily tested...).
  -r    Remove the ".####" decomposed files after a successful run.
  -n #  Input filename extensions start with number #### instead of 0000.
  -k #  Blocking factor. k records are read from an input file at a time.
        Valid values are between 0 and {}. For a given input, the maximum
        permissible value for k is min(total number of records, {}).
        Setting k to zero will set the blocking factor to this maximum
        permissible value. Setting k to a value higher than this value,
        will make the system implictly set k to the highest permissible value.
        A value of 1 for k disables blocking. This is the default behavior.
        Blocking often improves performance, but increases the peak memory
        footprint (by the blocking factor). Beware of running out of
        available physical memory and causing swapping to disk due to
        large blocking factors and/or large input datasets.
        A value of 10 for k has worked well on many input datasets.
        See -x for estimating memory usage for a given input set.
  -e #  Ending number #### of a specified range of input filename extensions.
        Files within the range do not have to be consecutively numbered.
  -h #  Add a specified number of bytes of padding at the end of the header.
  -64   Create netCDF output files with the 64-bit offset format.
  -n4   Create netCDF output files in NETCDF4_CLASSIC mode (no v4 enhanced features).
  -m    Initialize output variables with a "missing_value" from the variables
        of the first input file instead of the default 0 value.
  -x    Print an estimate for peak memory resident size in (MB) and exit.
        No output file will be created. Setting -x automatically sets
        the blocking factor (-k) to 1. Any value set for -k on the
        command-line will be ignored. To estimate memory usage for a
        a different blocking factor, simply multiply the estimate by k.

mppnccombine joins together an arbitrary number of netCDF input files, each
containing parts of a decomposed domain, into a unified netCDF output file.
An output file must be specified and it is assumed to be the first filename
argument.  If the output file already exists, then it will not be modified
unless the option is chosen to append to it.  If no input files are specified
then their names will be based on the name of the output file plus the default
numeric extension ".0000", which will increment by 1.  There is an option for
starting the filename extensions with an arbitrary number instead of 0.  There
is an option for specifying an end to the range of filename extension numbers;
files within the range do not have to be consecutively numbered.  If input
files are specified then names will be used verbatim.

A value of 0 is returned if execution completed successfully; a value of 1
otherwise.

""".format(__version__, MAX_BF, MAX_BF)


def check_mem_usage():
    pagesize = resource.getpagesize()


def nccombine(verbose, print_mem_usage, force, append_nc, remove_input,
              n_start, bf, n_end, header_pad, use_nc3_64offset,
              use_nc4_classic, missing, mem_dry_run, output_filename,
              input_filenames):

    # Set NetCDF output type
    assert not (use_nc3_64offset and use_nc4_classic)

    if use_nc3_64offset:
        nc_format = 'NETCDF3_64BIT'
    elif use_nc4_classic:
        nc_format = 'NETCDF4_CLASSIC'
    else:
        nc_format = 'NETCDF3_CLASSIC'

    if append_nc:
        output_nc = nc.Dataset(output_filename, 'r', format=nc_format)
    else:
        if os.path.isfile(output_filename):
            print('Error: output file seems to exist already!')
            return 1
        else:
            output_nc = nc.Dataset(output_filename, 'w', format=nc_format)

    # Construct the input filename list if not provided
    if not input_filenames:
        # TODO: This is a quick version
        input_filenames = [f for f in os.listdir(os.curdir)
                           if f.startswith(output_filename + '.')]

    #=============================

    # Create the tiled dimensions
    header_fname = input_filenames[0]
    header_nc = nc.Dataset(header_fname, 'r')

    # Construct composite dimensions
    header_dims = (v for v in header_nc.variables if v in header_nc.dimensions)

    for v_name in header_dims:
        v_nc = header_nc.variables[v_name]
        d_nc = header_nc.dimensions[v_name]

        if hasattr(v_nc, 'domain_decomposition'):
            bnds = v_nc.domain_decomposition.tolist()
            d_len = 1 + bnds[1] - bnds[0]
            output_nc.createDimension(v_name, d_len)
        elif d_nc.isunlimited():
            output_nc.createDimension(v_name, None)
        else:
            output_nc.createDimension(v_name, len(d_nc))

    # Copy global attributes
    for attr in header_nc.ncattrs(): 
        if attr == 'filename':
            attr_val = output_filename
        else:
            attr_val = header_nc.getncattr(attr)
        output_nc.setncattr(attr, attr_val)

    header_nc.close()
 
    # Gather the tile domain index bounds
    # TODO: Skip first entry?

    var_bounds = {}
    for input_fname in input_filenames:
        input_nc = nc.Dataset(input_fname, 'r')

        input_var_bnds = {}
        for v in split_dims:
            bnds = input_nc.variables[v].domain_decomposition.tolist()
            input_var_bnds[v] = bnds

        var_bounds[input_fname] = input_var_bnds
        input_nc.close()

    #============================

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

    parser.add_argument('output_filename', metavar='output.nc')
    parser.add_argument('input_filenames', metavar='input', nargs='*')

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
