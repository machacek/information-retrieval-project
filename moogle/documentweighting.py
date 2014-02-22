import re
import argparse

from math import log, sqrt
from collections import namedtuple, defaultdict


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

#
# Term frequency 
#

class NaturalTermFrequency(IndexMixin):
    def term_frequency(self, term, docid, tf):
        return tf

class LogarithmTermFrequency(IndexMixin):
    def term_frequency(self, term, docid, tf):
        return 1 + log(tf)

class AugmentedTermFrequency(IndexMixin):
    def index_ready(self):
        self.max_tf = defaultdict(int)
        for posting_list in self.inverted_index.values():
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
        for posting_list in self.inverted_index.values():
            for posting in posting_list:
                acc[posting.docid] += posting.tf
                counts[posting.docid] += 1
        self.ave_tf = {}
        for docid, count in counts.items():
            self.ave_tf[docid] = acc[docid]/count 
        super().index_ready()

    def term_frequency(self, term, docid, tf):
        return (1 + log(tf)) / (1 + self.ave_tf[docid])

term_frequency_classes = {
        'n' : NaturalTermFrequency,
        'l' : LogarithmTermFrequency,
        'a' : AugmentedTermFrequency,
        'b' : BooleanTermFrequency,
        'L' : LogAveTermFrequency,
        }
#
# Document frequency
#

class NoDocumentFrequency(IndexMixin):
    def document_frequency(self, term):
        return 1

class IdfDocumentFrequency(IndexMixin):
    def document_frequency(self, term):
        df_t = len(self.inverted_index[term])
        return log( self.inverted_index.N / df_t )

class ProbIdfDocumentFrequency(IndexMixin):
    def document_frequency(self, term):
        df_t = len(self.inverted_index[term])
        return max(0, log((self.inverted_index.N - df_t) / df_t))

document_frequency_classes = {
        'n' : NoDocumentFrequency,
        't' : IdfDocumentFrequency,
        'p' : ProbIdfDocumentFrequency,
        }

#
# Normalization
#

class NoNormalization(IndexMixin):
    def vector_norm(self, docid):
        return 1

class CosineNormalization(IndexMixin):
    def index_ready(self):
        sum_of_squares = defaultdict(int)
        for term, posting_list in self.inverted_index.items():
            # optimization: we don't use self.weight method here
            document_frequency = self.document_frequency(term)
            for docid, tf in posting_list:
                term_frequency = self.term_frequency(term, docid, tf)
                weight = document_frequency * term_frequency
                sum_of_squares[docid] += weight ** 2

        self.vector_norms = {}
        for docid, sum in sum_of_squares.items():
            self.vector_norms[docid] = sqrt(sum) 

    def vector_norm(self, docid):
        return self.vector_norms[docid]

class PivotedUniqueNormalization(IndexMixin):
    pass

normalization_classes = {
        'n' : NoNormalization,
        'c' : CosineNormalization,
        }

#
# Factory method
#

choices = [
        "".join(sorted(term_frequency_classes.keys())),
        "".join(sorted(document_frequency_classes.keys())),
        "".join(sorted(normalization_classes.keys())),
        ]
document_weighting_pattern = "[" + "][".join(choices) + "]"
config_re = re.compile(r"^%s$" % document_weighting_pattern)

def document_weighting_factory(config_str):
    # Check that configuration string is valid
    if not config_re.match(config_str):
        raise argparse.ArgumentTypeError(
                "config string %s is not valid, it should match this pattern:\n%s"
                % (config_str, weighting_metavar))

    DocumentWeighting = namedtuple("DocumentWeighting", ["term_frequency","document_frequency","normalization"])
    return DocumentWeighting(
            term_frequency = term_frequency_classes[config_str[0]],
            document_frequency = document_frequency_classes[config_str[1]],
            normalization = normalization_classes[config_str[2]],
            )

