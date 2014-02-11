from factory import Factory

from operator import attrgetter

termclassifier_factory = Factory({
    'wordforms' : attrgetter('form'),
    'lemmas'    : attrgetter('lemma'),
    })
