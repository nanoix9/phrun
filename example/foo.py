#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import phrun

def main():
    app = phrun.App('foo')
    app.get_runner() \
            .add_phase('src', lambda param: [int(i) for i in param]) \
            .add_phase('add', lambda x: x[0] + x[1]) \
            .add_phase('pow', lambda x: x ** 2) \
            .add_phase('print', lambda x: print(x))

    app.run()

if __name__ == '__main__':
    main()
