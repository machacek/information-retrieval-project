import os
from itertools import imap
from multiprocessing import Pool

from config import config
from document_topic import Document, Topic

class Collection(object):
    def __init__(self, list_file, prefix=''):
        self.names_list = [os.path.join(prefix, file_name.strip()) for file_name in list_file]

    def __iter__(self):
        pool = Pool(min(config.workers,len(self.names_list)))
        return pool.imap(self.type, self.names_list)
        pool.close()
        #return imap(self.type, self.names_list)

class TopicCollection(Collection):
    type = Topic

class DocumentCollection(Collection):
    type = Document
