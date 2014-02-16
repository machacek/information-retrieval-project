from math import log

from config import config
from collections import defaultdict, namedtuple, Counter


Posting = namedtuple("Posting", ["docid","tf"])

class InvertedIndex(
        defaultdict,
        config.weighting.term_frequency,
        config.weighting.document_frequency,
        config.weighting.normalization
        ):

    def __init__(self, documents=[], tire="text"):
        super(InvertedIndex, self).__init__(list)
        self.tire = tire
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
        section = getattr(document, self.tire)
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
        normalized_log_scores = Counter()
        for docid, score in scores.items():
            norm = self.vector_norm(docid)
            normalized_log_scores[docid] = log(score) - log(norm)

        return normalized_log_scores.most_common()




