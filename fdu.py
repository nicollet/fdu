#! /usr/bin/env python3

import glob
import os.path
import copy
import sys

def human_size(size):
    unit = ''
    units = ['KB', 'MB', 'GB', 'TB']
    while size > 1024 and len(units) > 0:
        size /= 1024
        unit = units.pop(0)
    return "%.2f %s" % (size, unit)

def write(fname, args):
    args_ = args
    args_.files = ["%s/*" % fname]
    size = fdu(args_, silent=True)
    fsize = "%s/.SIZE" % fname
    with open(fsize, 'w') as f:
        f.write("%s\n" % size)
    return size

def fdu(args, silent=False):
    total_size = 0
    for file_ in args.files:
        for f in glob.glob(file_):
            size = 0
            if os.path.isdir(f) and not os.path.ismount(f):
                if args.update:
                    size = write(f, args)
                else:
                    try:
                        with open("%s/.SIZE" % f, 'r') as f_:
                            size = int(f_.read())
                    except IOError:
                        size = write(f, args)
                if f[-1] != "/":
                    f += '/'
            else:
                try:
                    size = os.path.getsize(f)
                except OSError:
                    sys.stderr.write("can't get size: %s" % f)
            if not silent:
                print("%s %s" % (f, human_size(size)))
            total_size += size
    if not silent:
        print("total: %s" % (human_size(total_size)))
    return total_size


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--update", help="recompute every .SIZE", action="store_true")
#parser.add_argument("-p", "--update-parent", help="recompute this .SIZE and all its parent", action="store_true")
#parser.add_argument("-s", "--safe-write", help="use fdatasync", action="store_true")
parser.add_argument('files', metavar='FILE', nargs='*')
args = parser.parse_args()

fdu(args)

# vim: set ts=4 sw=4 expandtab:
