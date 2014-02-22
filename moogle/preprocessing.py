from factory import Factory
from operator import attrgetter
from collections import Counter

#
# Casing
#
caser_factory = Factory(init=False, types={
        'yes' : lambda x: x.lower(),
        'no' : lambda x: x,
    })

#
# Stopwords
#
class MostFrequentStopwords(object):
    def __init__(self, count = 20):
        self.count = int(count)

    def initialize_from_zone_index(self, zone_index):
        term_counter = Counter()
        for index in zone_index.values():
            for term, posting_list in index.items():
                sum = 0
                for posting in posting_list:
                    sum += posting.tf
                term_counter[term] += sum

        self.stopwords = dict(term_counter.most_common(self.count))

    def __contains__(self, item):
        return self.stopwords.__contains__(item)
        
stopwords_factory = Factory({
        'none' : set,
        'mostfrequent' : MostFrequentStopwords,
        'custom' : lambda *x: set(x),
    })

#
# Termclassifying
#
termclassifier_factory = Factory(init=False, types={
    'forms'         : attrgetter('form'),
    'lemmas'        : attrgetter('lemma'),
    'shortlemmas'   : lambda x: x.lemma.split('_')[0]
    })
