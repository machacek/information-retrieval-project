import re
import argparse

from math import log
from collections import namedtuple, defaultdict

weighting_pattern = "[nlab][ntp][ncu]\.[nlab][ntp][ncu]"
config_re = re.compile(r"^%s$" % weighting_pattern)



def weighting_factory(config_str):

    # Check that configuration string is valid
    if not config_re.match(config_str):
        raise argparse.ArgumentTypeError(
                "config string %s is not valid, it should match this pattern:\n%s"
                % (config_str, weighting_metavar))

    WeightingConfig = namedtuple("WeightingConfig", ["document","query"])
    return WeightingConfig(
            document = document_weighting_factory(config_str[0:3]),
            query = None,
        )

#
# Document weighting
#
# Please note, that we are using the term "term frequency" in two
# different (but possibly related) meanings:
#
#    1) tf_t,d - number of terms t in document d
#
#    2) local weight of the term in given document
#
# Please note, that we are using the term "document frequency" in two
# different (but possibly related) meanings:
#
#    1) df_t - number of documents in which the term t occurs
#
#    2) global weight of the term (is the same for all documents)
#
# See http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf, page 128
#

class IndexMixin(object):
    def index_ready(self):
        pass

# Term frequency 

class NaturalTermFrequency(IndexMixin):
    def term_frequency(self, term, docid, tf):
        return tf

class LogarithmTermFrequency(IndexMixin):
    def term_frequency(self, term, docid, tf):
        return 1 + log(tf)

class AugmentedTermFrequency(IndexMixin):
    def index_ready(self):
        self.max_tf = defaultdict(int)
        for posting_list in self.values():
            for posting in posting_list:
                self.max_tf[posting.docid] = max(self.max_tf[posting.docid], posting.tf)
        super().index_ready()

    def term_frequency(self, term, docid, tf):
        return 0.5 + 0.5*(tf/self.max_tf[docid])

class BooleanTermFrequency(IndexMixin):
    def term_frequency(self, term, docid, tf):
        if tf > 0:
            return 1
        else:
            return 0
            # This branch should be never reached, because posting list should not contain
            # counts less than one. For sure.

class LogAveTermFrequency(IndexMixin):
    def index_ready(self):
        acc = defaultdict(int)
        counts = defaultdict(int) 
        for posting_list in self.values():
            for posting in posting_list:
                acc[posting.docid] += posting.tf
                counts[posting.docid] += 1
        self.ave_tf = {}
        for docid, count in counts:
            self.ave_tf[docid] = acc[docid]/count 
        super().index_ready()

    def term_frequency(self, term, docid, tf):
        return (1 + log(tf)) / (1 + self.ave_tf[docid])

# Document frequency

class NoDocumentFrequency(IndexMixin):
    def document_frequency(self, term):
        return 1

class IdfDocumentFrequency(IndexMixin):
    def document_frequency(self, term):
        df_t = len(self[term])
        return log( self.N / df_t )

class ProbIdfDocumentFrequency(IndexMixin):
    def document_frequency(self, term):
        df_t = len(self[term])
        return max(0, log((self.N - df_t) / df_t))

# Normalization

class NoNormalization(IndexMixin):
    def doc_vector_length(self, docid):
        return 1

class CosineNormalization(IndexMixin):
    def index_ready(self):
        # TODO

    def doc_vector_length(self, docid):
        return self.doc_vector_lengths[docid]


def document_weighting_factory(str):





