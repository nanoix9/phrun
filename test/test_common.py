#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

from phrun.cache import Cache
from phrun.runner import Runner

Cache.set_root_dir('.')

def test_cache():
    cache = Cache.get_cache('test_common')
    cache.set('int', 100)
    assert cache.get('int') == 100
    cache.clean()

def test_runner():
    r = Runner().use_cache('test_common')
    r.add_phase('src', lambda: (1, 2)) \
        .add_phase('add', lambda x: x[0] + x[1]) \
        .add_phase('pow', lambda x: x ** 2)

    out = r.run()
    print(out)
    out = r.run_from(1)
    print(out)

def main():
    # test_cache()
    test_runner()
    return

if __name__ == '__main__':
    main()
