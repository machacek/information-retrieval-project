from utils import Factory

class MostFrequentStopwords(object):
    pass

stopwords_factory = Factory({
    'none' : [],
    'mostfrequent' : MostFrequentStopwords,
    })

