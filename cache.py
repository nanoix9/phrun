#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pickle
import os
import os.path
import shutil
from .log import logger

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), '.phrun', 'cache')
DEFAULT_CACHE_SUFFIX = '.cache'

class Cache(object):

    _settings = {
        'root_dir': DEFAULT_CACHE_DIR,
        'cache_suffix': DEFAULT_CACHE_SUFFIX,
    }
    _caches = {}

    def __init__(self, name, root_dir=None):
        if root_dir is None:
            root_dir = self._get_setting('root_dir')
        self._name = name
        self._root_dir = root_dir

    @property
    def name(self):
        return self._name

    def set(self, key, data):
        # print(key, data)
        path = self._get_path(key)
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
            logger.info('create new directory for cache "%s": "%s"' % (self._name, dirname))
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        #else:
        #    raise RuntimeError('directory "%s" doesnt exists' % dirname)
        logger.info('dump to cache file {}'.format(path))
        return self

    def has(self, key):
        path = self._get_path(key)
        return os.path.isfile(path)

    def get(self, key):
        if self.has(key):
            path = self._get_path(key)
            with open(path, 'rb') as f:
                data = pickle.load(f)
            logger.info('load from cache file {}'.format(path))
            return data
        else:
            raise RuntimeError('cache {} does not have key "{}"' \
                .format(self._name, key))

    def clean(self, remove_dir=True):
        cdir = self._get_cache_dir()
        if remove_dir:
            logger.info('deleting cache directory: {}'.format(cdir))
            shutil.rmtree(cdir)
        else:
            raise NotImplementedError()

    def _get_cache_dir(self):
        return os.path.join(self._root_dir,
            self._name + self._get_setting('cache_suffix'))

    def _get_path(self, key):
        return os.path.join(self._get_cache_dir(), key)

    @classmethod
    def get_cache(cls, cache_name, **kwds):
        if cache_name not in cls._caches:
            cls._caches[cache_name] = Cache(cache_name, **kwds)
        return cls._caches[cache_name]

    @classmethod
    def remove_cache(cls, cache_name, **kwds):
        if cache_name not in cls._caches:
            logger.warning('cache not exists: {}'.format(cache_name))
            return
        cls._caches[cache_name].clean(**kwds)
        del cls._caches[cache_name]

    @classmethod
    def set_root_dir(cls, dir):
        # print(dir)
        cls._set_setting('root_dir', dir)

    @classmethod
    def _set_setting(cls, name, value):
        cls._settings[name] = value

    @classmethod
    def _get_setting(cls, name):
        return cls._settings[name]

def main():
    return

if __name__ == '__main__':
    main()

