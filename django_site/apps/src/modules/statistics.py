"""
@Desc:
"""

import json

class Stat(object):
    def __init__(self, name):
        self.name = name
        self._attrs = dict()  # collect anything needed

    def attrs(self):
        return self._attrs

    def add_attr(self, key, val):
        self._attrs[key] = val
        return self

    def __repr__(self):
        info = {'stat name', self.name,
                'attrs', self.attrs}
        return json.dumps(info, indent=4)

class Statistics(object):
    collections = dict()

    @classmethod
    def add(cls, stat: Stat):
        if stat.name in cls.collections:
            return False
        else:
            cls.collections[stat.name] = stat.attrs()
            return True

    @classmethod
    def update(cls, stat: Stat, key, val):
        if stat.name not in cls.collections:
            return False
        else:
            cls.collections[stat.name][key] = val
            return True

    @classmethod
    def repr(cls):
        return json.dumps(cls.collections, indent=4)
