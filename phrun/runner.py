#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from .log import logger
from .cache import Cache
from .phase import Phase

NO_ARG = object()
# NO_ARG.__str__ = lambda self: 'NO ARGUMENT'
# NO_ARG.__repr__ == NO_ARG.__str__

class Runner(object):

    def __init__(self):
        self._phases = []
        self._name_index_map = {}
        self._cache = None

    def use_cache(self, cache=None, ignore_cache_failure=False):
        if isinstance(cache, Cache):
            self._cache = cache
        elif isinstance(cache, str):
            self._cache = Cache.get_cache(cache)
        else:
            raise ValueError('invalid cache: {}'.format(cache))
        logger.info('using cache at {}'.format(self._cache._get_cache_dir()))
        self.ignore_cache_failure = ignore_cache_failure
        return self

    def run(self, params=NO_ARG):
        return self.run_from_index(0, params=params)

    def run_from(self, phase_i, params=NO_ARG):
        if isinstance(phase_i, int):
            start_index = phase_i
        elif isinstance(phase_i, str):
            start_index = self.get_phase_index(phase_name)
        else:
            raise ValueError('invalid start phase specifier: {}'.format(phase_i))

        return self.run_from_index(start_index, params=params)

    def run_from_index(self, index, params=NO_ARG):
        logger.info('start to run from phase {}: {}' \
            .format(index, self._phases[index].name))
        x = params
        if x is NO_ARG and index > 0:
            x = self._get_from_cache(index - 1)
        for i, phase in enumerate(self._phases):
            if i < index:
                logger.info('skip phase {}: {}'.format(i, phase.name))
                continue
            logger.info('runing phase {}: {}'.format(i, phase.name))
            x = self._run_phase(i, phase, x)
            self._set_to_cache(i, x)
        return x

    def _run_phase(self, index, phase, args):
        # print(index, phase.name, args)
        if args is NO_ARG:
            ret = phase.run()
        else:
            ret = phase.run(args)
        return ret

    def _cache_enabled(self):
        return self._cache is not None

    def _get_from_cache(self, index):
        key = self._cache_key(index)
        if self._cache_enabled() and self._cache.has(key):
            try:
                return self._cache.get(key)
            except Exception as e:
                if self.ignore_cache_failure:
                    logger.warning('failed to read "%s" from cache "%s", message: %s', \
                            key, self._cache.name, repr(e))
                else:
                    raise
        else:
            return NO_ARG

    def _set_to_cache(self, index, value):
        if self._cache_enabled():
            key = self._cache_key(index)
            try:
                self._cache.set(key, value)
            except Exception as e:
                if self.ignore_cache_failure:
                    logger.warning('failed to write "%s" to cache "%s", message: %s', \
                            key, self._cache.name, repr(e))
                else:
                    raise
        return self

    def _cache_key(self, index):
        return self.get_phase_by_index(index).name + '.out'

    def get_phase_index(self, phase_name):
        if phase_name not in self._name_index_map:
            raise ValueError('cannot find phase "{}"'.format(phase_name))
        return self._name_index_map[phase_name]

    def get_phase(self, phase_name):
        return self.get_phase_by_index[self.get_phase_index(phase_name)]

    def get_phase_by_index(self, index):
        return self._phases[index]

    def add_phase(self, *args):
        if len(args) == 1 and isinstance(args[0], Phase):
            phase = args[0]
            if self.has_phase(phase.name):
                raise ValueError('phase "{}" already exists'.format(phase.name))
            self._phases.append(phase)
            self._name_index_map[phase.name] = len(self._phases) - 1
            return self
        else:
            if len(args) == 2 and isinstance(args[0], str):
                name = args[0]
                func = args[1]
            elif len(args) == 1:
                name = args[0].__name__
                logger.warning('phase name not specified, use "{}"' \
                    .format(name))
                func = args[0]
            else:
                raise ValueError('invalid arguments: {}'.format(args))

            if not hasattr(func, '__call__'):
                raise ValueError('phase function must be callable but got {}' \
                    .format(func))

            phase = Phase(name, func)
            return self.add_phase(phase)

    def has_phase(self, name):
        return name in self._name_index_map

def main():
    return

if __name__ == '__main__':
    main()
