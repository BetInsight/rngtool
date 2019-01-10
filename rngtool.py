#!/usr/bin/env python

import sys
import argparse
import random
import time
import struct
import math


def str2long(v):

    try:
        if v.upper().find('B') != -1:
            return long(v, 2)
    except ValueError:
        pass

    try:
        if v.upper().find('X') != -1:
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
    parser.add_argument("-f",
                        help="the name of output file",
                        dest="output_filename",
                        metavar="FILE")
    parser.add_argument("-sf",
                        help="save used seed to filename",
                        dest="seed_output_filename",
                        metavar="FILE")
    parser.add_argument("-r",
                        help="range of generated numbers",
                        dest="seq_range",
                        metavar="RANGE",
                        type=str2long)
    parser.add_argument("-s",
                        help="initial SEED (generator input value)",
                        dest="seed",
                        metavar="SEED",
                        type=str2long)
    parser.add_argument("-rw",
                        help="raw output from RNG",
                        dest="raw_output",
                        action='store_true')
    return parser


def rng_tool(args, f_output=None, f_output_raw=None):

    if args.seed:
        seed = args.seed
    else:
        # use fractional seconds
        seed = long(time.time() * 256)

    seq_length = args.seq_length

    if args.raw_output or f_output_raw:
        seq_range = 256
        seq_length = long(math.floor(seq_length / 8))
    elif args.seq_range:
        seq_range = args.seq_range
    else:
        seq_range = sys.maxsize

    if args.seed_output_filename:
        with open(args.seed_output_filename, 'w') as f_output:
            f_output.write(str(seed))
    rnd = random.Random(seed)

    if not f_output and args.output_filename and not args.raw_output:
        f_output = open(args.output_filename, 'w')

    if not f_output_raw and args.output_filename and args.raw_output:
        f_output_raw = open(args.output_filename, 'wb')

    for _ in xrange(seq_length):
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
