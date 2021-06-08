# mem_stat.py - memory usage statistics for python objects

from collections import Mapping, Container
from sys import getsizeof

def get_mem_size(o, ids):
    d = deep_getsizeof
    if id(o) in ids:
     return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str) or isinstance(0, unicode):
     return r

    if isinstance(o, Mapping):
     return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())

    if isinstance(o, Container):
     return r + sum(d(x, ids) for x in o)

    return r
