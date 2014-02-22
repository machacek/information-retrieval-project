import os
from collections import Counter
from multiprocessing import Pool

from document import Document
from topic import Topic

def init_type(arg_tuple):
    type = arg_tuple[0]
    args = arg_tuple[1:]
    return type(*args)

class Collection(object):
    def __init__(self, list_file, case, classes, prefix='', workers=20):
        self.case = case
        self.classes = classes
        self.names_list = [os.path.join(prefix, file_name.strip()) for file_name in list_file]
        self.workers = workers

    def __iter__(self):
        args = ((self.type, name, self.case, self.classes) for name in self.names_list)
        pool = Pool(min(self.workers,len(self.names_list)))
        return pool.imap(init_type, args)
        pool.close()

class TopicCollection(Collection):
    type = Topic

class DocumentCollection(Collection):
    type = Document
