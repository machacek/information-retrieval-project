from math import log

from collections import defaultdict, namedtuple, Counter

import warnings


Posting = namedtuple("Posting", ["docid","tf"])

class InvertedIndex(defaultdict):
    def __init__(self, zone="text"):
        super(InvertedIndex, self).__init__(list)
        self.zone = zone
        self.N = 0

    def index_document(self, document):
        docid = document.docid

        # Add postings to posting lists
        section = getattr(document, self.zone)
        for term, tf in section.items():
            self[term].append(Posting(docid, tf))
        self.N += 1

class ZoneInvertedIndex(defaultdict):
    def __init__(self, documents=[], zones=("title","heading","text")):
        super(ZoneInvertedIndex, self).__init__(InvertedIndex)
        for zone in zones:
            self[zone] = InvertedIndex(zone)
        self.index_documents(documents)
        
    def index_documents(self, documents):
        for document in documents:
            for index in self.values():
                index.index_document(document)

    def init_stopwords(self, stopwords):
        try:
            stopwords.initialize_from_zone_index(self)
        except AttributeError:
            pass

def get_retrieval_system_type(weighting):
    class RetrievalSystem(
            weighting.term_frequency,
            weighting.document_frequency,
            weighting.normalization
            ):

        def __init__(self, inverted_index, stopwords):
            self.inverted_index = inverted_index
            self.stopwords = stopwords
            self.index_ready()
        
        def weight(self, term, docid, tf):
            "Returns component of the matrix given by term and document"
            term_frequency = self.term_frequency(term, docid, tf)
            document_frequency = self.document_frequency(term)
            return term_frequency * document_frequency
                
        def retrieve(self, query):

            # We are going to process term at a time
            scores = Counter()
            for term in query.elements():

                if term in self.stopwords or term not in self.inverted_index:
                    continue

                # optimization: we don't use self.weight method here
                document_frequency = self.document_frequency(term)
                for docid, tf in self.inverted_index[term]:
                    term_frequency = self.term_frequency(term, docid, tf)
                    scores[docid] += term_frequency * document_frequency

            # Normalizing
            normalized_scores = Counter()
            for docid, score in scores.items():
                norm = self.vector_norm(docid)
                normalized_scores[docid] = score / norm 
            return normalized_scores
    return RetrievalSystem

class ZoneRetrievalSystem(defaultdict):
    def __init__(self, zone_inverted_index, zone_weights, stopwords, document_weighting):
        RetrievalSystem = get_retrieval_system_type(document_weighting)
        super(ZoneRetrievalSystem, self).__init__(RetrievalSystem)
        self.zone_weights = zone_weights
        for zone, inverted_index in zone_inverted_index.items():
            self[zone] = RetrievalSystem(inverted_index, stopwords)

    def retrieve(self, query):
        result = Counter()
        for zone, retrieval_system in self.items():
            weight = self.zone_weights[zone]
            zone_result = retrieval_system.retrieve(query)
            for docid in zone_result:
                zone_result[docid] *= weight
            result += zone_result
        return result
