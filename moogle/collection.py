import os
from collections import Counter
from multiprocessing import Pool

from config import config
from document import Document
from topic import Topic

pool = Pool(config.workers)

class Collection(object):
    def __init__(self, list_file):
        self.names_list = [os.path.join(config.prefix, file_name.strip()) for file_name in list_file]

    def __iter__(self):
        return pool.imap(self.type, self.names_list)

class TopicCollection(Collection):
    type = Topic

class DocumentCollection(Collection):
    type = Document

    def get_merged_counts(self):
        title_counter = Counter()
        heading_counter = Counter()
        text_counter = Counter()

        for document in self:
            title_counter.update(document.title)
            heading_counter.update(document.heading)
            text_counter.update(document.text)

        return (title_counter, heading_counter, text_counter)
