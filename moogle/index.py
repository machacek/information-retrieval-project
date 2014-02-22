from math import log

from config import config
from collections import defaultdict, namedtuple, Counter

import warnings


Posting = namedtuple("Posting", ["docid","tf"])

class InvertedIndex(
        defaultdict,
        config.weighting.term_frequency,
        config.weighting.document_frequency,
        config.weighting.normalization
        ):

    def __init__(self, documents=[], zone="text"):
        super(InvertedIndex, self).__init__(list)
        self.zone = zone
        self.N = 0
        self.index_documents(documents)

    def index_documents(self, documents):
        for document in documents:
            self.__index_document(document)
        self.index_ready()

    def index_document(self, document):
        self.__index_document(document)
        self.index_ready()

    def __index_document(self, document):
        docid = document.docid

        # Add postings to posting lists
        section = getattr(document, self.zone)
        for term, tf in section.items():
            self[term].append(Posting(docid, tf))
        self.N += 1
    
    def weight(self, term, docid, tf):
        "Returns component of the matrix given by term and document"
        document_frequency = self.document_frequency(term)
        return term_frequency * document_frequency
            
    def retrieve(self, query):

        # We are going to process term at a time
        scores = Counter()
        for term in query.elements(): 
            # optimization: we don't use self.weight method here
            document_frequency = self.document_frequency(term)
            for docid, tf in self[term]:
                term_frequency = self.term_frequency(term, docid, tf)
                scores[docid] += term_frequency * document_frequency

        # Normalizing
        normalized_scores = Counter()
        for docid, score in scores.items():
            norm = self.vector_norm(docid)
            normalized_scores[docid] = score / norm 
        return normalized_scores

class ZoneIndex(object):
    def __init__(documents, zones):
        self.indexes = []
        self.weights = []
        for zone, weight in zones:
            self.indexes.append(InvertedIndex(documents, zone=zone))
            self.weights.append(weight)

    def index_documents(self, documents):
        for index in self.indexes:
            index.index_documents(documents)
    
    def index_document(self, document):
        for index in self.indexes:
            index.index_document(document)

    def retrieve(self, query):
        result = Counter()
        for index, weight in zip(self.indexex, self.weights):
            zone_result = index.retrieve(query)
            for docid in zone_result:
                zone_result[docid] *= wei
            result += zone_result
        return result





