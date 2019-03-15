#!/usr/bin/env python

import sys
import argparse
import random
import time
import struct
import math
import re

try:
    # Python 2 forward compatibility
    range = xrange
except NameError:
    long = int


def str2long(v):

    try:
        if v.upper().startswith('0B'):
            return long(v, 2)
    except ValueError:
        pass

    try:
        if v.upper().startswith('0X'):
            return long(v, 16)
    except ValueError:
        pass

    try:
        if re.match("^[0-9A-F]+$", v.upper()) and \
                not re.match("^[0-9]+$", v.upper()):
            return long(v, 16)
    except ValueError:
        pass

    try:
        return long(v, 10)
    except ValueError:
        raise argparse.ArgumentTypeError('Long value expected.')


def get_argparser():
    parser = argparse.ArgumentParser(description='RNG Tool')
    parser.add_argument("-n",
                        help="length of sequence",
                        dest="seq_length",
                        metavar="NUM",
                        type=str2long,
                        required=True)
    parser.add_argument("-f", "-o",
                        help="the name of output file",
                        dest="output_filename",
                        metavar="FILE")
    parser.add_argument("-sf",
                        help="save used seed to filename",
                        dest="seed_output_filename",
                        metavar="FILE")
    parser.add_argument("-r", "-range",
                        help="range of generated numbers",
                        dest="seq_range",
                        metavar="RANGE",
                        type=str2long)
    parser.add_argument("-s", "-seed",
                        help="initial SEED (generator input value)",
                        dest="seed",
                        metavar="SEED",
                        type=str2long)
    parser.add_argument("-rw", "-raw",
                        help="raw output from RNG",
                        dest="raw_output",
                        action='store_true')
    parser.add_argument("-chunks",
                        help="num of chunks",
                        dest="chunks",
                        metavar="NUM",
                        type=str2long)
    return parser


def rng_tool(args, f_output=None, f_output_raw=None):

    seq_length = args.seq_length

    if args.raw_output or f_output_raw:
        seq_range = 256
        seq_length = long(math.floor(seq_length / 8))
    elif args.seq_range:
        seq_range = args.seq_range
    else:
        seq_range = sys.maxsize

    if not f_output and args.output_filename and not args.raw_output:
        f_output = open(args.output_filename, 'w')

    if not f_output_raw and args.output_filename and args.raw_output:
        f_output_raw = open(args.output_filename, 'wb')

    if args.seed_output_filename:
        s_output = open(args.seed_output_filename, 'w')
    else:
        s_output = None

    chunks = args.chunks if args.chunks else 1

    if chunks > 1 and not s_output:
        raise argparse.ArgumentTypeError('Output file for seeds not defined')

    for _ in range(chunks):

        if args.seed is not None:
            seed = args.seed
        else:
            # use fractional seconds
            seed = long(time.time() * 256)

        if s_output:
            s_output.write('{}\n'.format(str(seed)))

        rnd = random.Random(seed)

        for _ in range(seq_length):
            rnd_value = rnd.randrange(seq_range)
            if f_output:
                f_output.write('{}\n'.format(rnd_value))
            elif f_output_raw:
                f_output_raw.write(struct.pack('>B', rnd_value))
            else:
                print(rnd_value)


if __name__ == '__main__':
    arg_parser = get_argparser()
    rng_tool(arg_parser.parse_args())
