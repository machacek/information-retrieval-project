import math

from config import config
from collections import defaultdict, namedtuple, Counter

Posting = namedtuple("Posting", ["docid","tf"])

class InvertedIndex(defaultdict):
    def __init__(self, documents=[], tire="text"):
        super(InvertedIndex, self).__init__(list)
        self.tire = tire
        self.lengths = dict()
        self.max_tf = defaultdict(lambda: 0)
        self.index_documents(documents)

    def index_documents(self, documents):
        for document in documents:
            self.index_document(document)

    def index_document(self, document):
        docid = document.docid

        # Add postings to posting lists
        section = getattr(document, self.tire)
        for term, tf in section:
            self[term].append(Posting(docid, tf))
            
            # Update max_tf
            self.max_tf[docid] = max(self.max_tf[docid], tf)
            
        # Store the length of the document
        self.lengths[docid] = document.section_length(self.tire)

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




