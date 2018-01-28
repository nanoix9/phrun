#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

from .runner import Runner
from .cache import Cache
from .log import logger

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('args', type=str, nargs='*',
                        help='other arguments passed to app')
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="increase output verbosity")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="enter debug mode")
    parser.add_argument("-p", "--phase", type=str, default='',
                        help="start running from which phase, specified by name")
    parser.add_argument("-i", "--phase-index", type=int, default=0,
                        help="start running from which phase, specified by index")
    parser.add_argument("--cache-root", default='.',
                        help="cache root directory")
    parser.add_argument("--cache-name", default='',
                        help="cache root directory")

    return parser

def parse_args(parser=None, argv=None):
    #print sys.argv
    if parser is None:
        parser = get_parser()
    if argv is None:
        argv = sys.argv[1:]
    #print argv
    #sys.exit()
    return parser.parse_args(argv)

class App(object):

    def __init__(self, name):
        self._name = name
        self._args = parse_args()
        logger.info('command line arguments: {}'.format(self._args))

        if self._args.cache_name != '':
            cache_name = self._args.cache_name
        else:
            cache_name = self._name

        if self._args.cache_root != '':
            cache = Cache.get_cache(cache_name, root_dir=self._args.cache_root)
        else:
            cache = Cache.get_cache(cache_name)

        self._runner = Runner().use_cache(cache)

    def get_runner(self):
        return self._runner

    def add_phase(self, *args, **kwds):
        self._runner.add_phase(*args, **kwds)
        return self

    def run(self):

        if self._args.phase != '':
            return self._runner.run_from(self._args.phase)
        else:
            return self._runner.run_from(self._args.phase_index)

def test1():
    argv = '-v -d other another'.split()
    print(argv, parse_args(argv=argv))
    argv = '-vvv -d'.split()
    print(argv, parse_args(argv=argv))

def main():
    test1()
    return

if __name__ == '__main__':
    main()
