#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import math

#
# Moogle imports
#
from whitespaceanalyzer import WhitespaceAnalyzer
from factory import Factory

#
# Lucene imports
#
import lucene
from lucene import SimpleFSDirectory, File, IndexReader, IndexSearcher, Term, Version
from lucene import Document, Field, QueryParser, StandardAnalyzer, BooleanQuery, BooleanClause
from lucene import TermQuery

class IndexSearcherWrapper(object):
    def __init__(self, location):
        lucene.initVM()
        directory = SimpleFSDirectory(File(location))
        self.reader = IndexReader.open(directory, True)
        self.searcher = IndexSearcher(self.reader)
        self.query_parser = QueryParser(Version.LUCENE_CURRENT, "text", WhitespaceAnalyzer())

    def search(self, topic, max=5000):
        query = self.query_parser.parse(topic.title)
        return self.searcher.search(query, max)


class ScorePair(object):
    def __init__(self, reader, field, term):
        self.count = 1
        self.idf = (1 + math.log(reader.numDocs()/(float(reader.docFreq(Term(field, term))) + 1))) ** 2
        self.field = field
        self.term = term

    def increment(self):
        self.count += 1

    def score(self):
        return math.sqrt(self.count) * self.idf
        # return self.idf

    def to_term(self):
        return Term(self.field, self.term)

class PseudoRelevanceSearcherWrapper(IndexSearcherWrapper):
    def __init__(self, location, top_n = 25):
        super(PseudoRelevanceSearcherWrapper, self).__init__(location)
        self.top_n = top_n

    def search(self, topic):

        query = self.query_parser.parse(topic.title)
        results = self.searcher.search(query, self.top_n)

        score_pairs = {} 
        for hit in results.scoreDocs:
            doc = self.searcher.doc(hit.doc)
            for field in ["title","heading", "text"]:
                terms = doc.get(field).split()
                for term in terms:
                    if (field, term) in score_pairs:
                        score_pairs[(field,term)].increment()
                    else:
                        score_pairs[(field,term)] = ScorePair(self.reader, field, term) # XXX

        top_terms = score_pairs.values()
        top_terms.sort(key=lambda x: x.score(), reverse=True)
        top_terms = top_terms[:25]

        # print([term.term for term in top_terms])


        bq = BooleanQuery() 
        query.setBoost(float(10000000))
        bq.add(query, BooleanClause.Occur.SHOULD)
        for score_pair in top_terms:
            term = score_pair.to_term()
            bq.add(TermQuery(term), BooleanClause.Occur.SHOULD)

        return self.searcher.search(bq, 5000)


searcher_factory = Factory(init = False, types={
    True    : PseudoRelevanceSearcherWrapper,
    False   : IndexSearcherWrapper,
    })
