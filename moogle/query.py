from factory import Factory
from operator import attrgetter
from collections import Counter

#
# Termclassifying
#
query_factory = Factory(init=False, types={
    'title'             : attrgetter('title'),
    'desc'              : attrgetter('desc'),
    'narr'              : attrgetter('narr'),
    'title+desc'        : lambda t: t.title + t.desc,
    'title+desc+narr'   : lambda t: t.title + t.desc + t.narr,

    })
