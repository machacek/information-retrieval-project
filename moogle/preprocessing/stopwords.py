from factory import Factory

class MostFrequentStopwords(object):
    def __init__(self, count = 20):
        self.count = int(count)
        self.stopwords = {}

    def initialize_from_data(self, bag_collection):
        title_counter, heading_counter, text_counter = bag_collection.get_merged_counts()

        # for now, we are going to merge all sections
        text_counter.update(title_counter)
        text_counter.update(heading_counter)
        
        self.stopwords = dict(text_counter.most_common(self.count))

    def __contains__(self, item):
        return self.stopwords.__contains__(item)
        

stopwords_factory = Factory({
        'none' : set(),
        'mostfrequent' : MostFrequentStopwords,
    })

