import math

from config import config
from collections import defaultdict, namedtuple, Counter

Posting = namedtuple("Posting", ["docid","tf"])

class InvertedIndex(defaultdict):
    def __init__(self, documents=[], tire="text"):
        super(InvertedIndex, self).__init__(list)
        self.tire = tire
        self.N = 0
        self.index_documents(documents)

    def index_documents(self, documents):
        for document in documents:
            self.index_document(document)
        self.index_ready()

    def index_document(self, document):
        docid = document.docid

        # Add postings to posting lists
        section = getattr(document, self.tire)
        for term, tf in section:
            self[term].append(Posting(docid, tf))
            
            # Update max_tf
            self.max_tf[docid] = max(self.max_tf[docid], tf)

        self.N += 1

    def weight(self, term, docid, tf)
        "Returns component of the matrix given by term and document"
        term_frequency = self.term_frequency(term, docid, tf)
        document_frequency = self.document_frequency(term)
        return term_frequency * document_frequency
            
    def retrieve(self, query):
        documents_scores = Counter()

        # we are going to process at a time
        for term in query.elements():

            df = len(self[term])
            N = len(self)
            idf = math.log(N/df)

            posting_list = self[term] 
            for docid, tf in posting_list:
                tf_idf = tf * idf
                documents_scores[docid] += tf_idf

        return documents_scores.most_common()




