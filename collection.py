from collections import Counter

from .document import DocumentVert
from .document import DocumentTokens
from .document import DocumentBag
from .topic import TopicVert
from .topic import TopicTokens
from .topic import TopicBag


class VertCollection(object):
    def __init__(self, prefix, list_file):
        self.prefix = prefix
        self.names_list = [file_name.strip() for file_name in list_file]

    def __iter__(self):
        for file_name in self.names_list:
            yield self.vert_type(self.prefix, file_name)

class TokensCollection(object):
    def __init__(self, vert_collection, config):
        self.vert_collection = vert_collection
        self.config = config

    def __iter__(self):
        for vert in self.vert_collection:
            yield self.tokens_type(vert, config)

class BagCollection(object):
    def __init__(self, tokens_collection):
        self.tokens_collection = tokens_collection

    def __iter__(self):
        for tokens in self.tokens_collection:
            yield self.bag_type(tokens)

class DocumentCollectionMixin(object):
    vert_type = DocumentVert
    tokens_type = DocumentTokens
    bag_type = DocumentBag

class TopicCollectionMixin(object):
    vert_type = TopicVert
    tokens_type = TopicTokens
    bag_type = TopicBag

class DocumentVertCollection(VertCollection, DocumentCollectionMixin):
    pass

class TopicVertCollection(VertCollection, TopicCollectionMixin):
    pass

class DocumentTokensCollection(TokensCollection, DocumentCollectionMixin):
    pass

class TopicTokensCollection(TokensCollection, TopicCollectionMixin):
    pass

class DocumentBagCollection(BagCollection, DocumentCollectionMixin):
    def get_merged_counts(self):
        title_counter = Counter()
        heading_counter = Counter()
        text_counter = Counter()

        for document in self:
            title_counter.update(document.title)
            heading_counter.update(document.heading)
            text_counter.update(document.text)

        return (title_counter, heading_counter, text_counter)

class TopicBagCollection(BagCollection, TopicCollectionMixin):
    pass
