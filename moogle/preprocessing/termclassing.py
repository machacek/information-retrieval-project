from factory import Factory

from operator import attrgetter

termclassifier_factory = Factory(init=False, types={
    'forms'         : attrgetter('form'),
    'lemmas'        : attrgetter('lemma'),
    'shortlemmas'   : lambda x: x.lemma.split('_')[0]
    })
