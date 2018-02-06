#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Phase(object):

    def __init__(self, name, func):
        if not isinstance(name, str) or name == '':
            raise ValueError('invalid phase name: "{}"'.format(name))
        self._name = name
        self._func = func

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise RuntimeError('phase name cannot be changed after creation')
        # self._name = value

    def run(self, *args, **kwds):
        return self._func(*args, **kwds)

def main():
    return

if __name__ == '__main__':
    main()
