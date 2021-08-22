"""
@reference:
python dict 保存为pickle格式
https://blog.csdn.net/rosefun96/article/details/90633786
"""

import os
import pickle
import json
from logging import DEBUG
from src.modules.logger import MyLogger

class Cache(object):
    def __init__(self, name, logger=None):
        self._name = name
        self._logger = logger if logger else MyLogger('cache', DEBUG)
        self._cache = dict()

    def add(self, key, val):
        if key in self._cache:
            self._logger.warning(f'key exits already, add failed.')
            return False
        else:
            self._cache[key] = val
            return True

    def put(self, key, val):
        self._cache[key] = val

    def get(self, key, default):
        return default if key not in self._cache else self._cache[key]

    def __iter__(self):
        for key in self._cache:
            yield key

    def __setitem__(self, key, val):
        self._cache[key] = val

    def __getitem__(self, key):
        return self._cache[key]

    def __repr__(self):
        return json.dumps(self._cache, indent=4)


class LocalCache(Cache):
    def __init__(self, name, logger=None):
        super(LocalCache, self).__init__(name, logger)
        self.local_path = ''

    def store(self, local_dir='./cache'):
        if not os.path.exists(local_dir):
            os.makedirs(local_dir, exist_ok=True)
            self._logger.warning(f'{local_dir} did not exist, and has been created now.')
        local_path = f'{os.path.join(local_dir, self._name)}.pkl'
        with open(local_path, 'wb') as fw:  # Pickling
            pickle.dump(self._cache, fw, protocol=pickle.HIGHEST_PROTOCOL)

        self.local_path = local_path

    def load(self, local_path=''):
        if not local_path:
            local_path = f'./cache/{self._name}.pkl'
        with open(local_path, 'rb') as fr:
            cache = pickle.load(fr)
        self._cache = cache

        self.local_path = local_path

    def smart_load(self, local_path=''):
        """
        :param local_path:
        :return:
        Don't raise an error if cache does not exis.
        """
        if not local_path:
            local_path = f'./cache/{self._name}.pkl'
        if os.path.exists(local_path):
            with open(local_path, 'rb') as fr:
                cache = pickle.load(fr)
                self._cache = cache

        self.local_path = local_path

    def clear(self):
        """
        :return:
        clear both cathe in memory and local.
        """
        self._cache = dict()
        if self.local_path:
            os.remove(self.local_path)
            self.local_path = ''

    @classmethod
    def load_from(cls, local_path):
        if os.path.exists(local_path):
            raise FileNotFoundError
        cache_name = os.path.basename(local_path).split('.')[0]
        new = LocalCache(cache_name)
        new.load(local_path)
        new.local_path = local_path  # record this local_path, it is useful when make clear.
        return new

