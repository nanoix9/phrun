#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from phrun.cache import Cache

Cache.set_root_dir('.')

def test_cache():
    cache = Cache.get_cache('test_common')
    cache.set('int', 100)
    assert cache.get('int') == 100
    cache.clean()

def main():
    test_cache()
    return

if __name__ == '__main__':
    main()
