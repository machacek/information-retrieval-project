import os
import sys
import warnings
from collections import Counter
from bs4 import BeautifulSoup

from preprocessing import termclassifier_factory, caser_factory

#warnings.simplefilter("always")

class VertItem(object):
    def __init__(self, line):
        self.valid = True
        fields = line.split(sep='\t')

        if len(fields) != 6:
            warnings.warn("Line \"%s\" has %s fields" % (line, len(fields)))
            self.valid = False
            return
        
        self.order  = int(fields[0])
        self.form   = fields[1]
        self.lemma  = fields[2]
        self.tag    = fields[3]

        # We are not doing this now
        # self.parrent  = fields[4]
        # self.syn_type = fields[5]

    def __bool__(self):
        return self.valid

class VertFormat(object):
    def __init__(self, path, caser, classifier):
        self.caser = caser_factory(caser)
        self.classifier = termclassifier_factory(classifier)
        with open(path, 'r') as file:
            try:
                soup = BeautifulSoup(file, "xml") 
                self.process_soup(soup)
            except ValueError:
                print("Error in file: %s" % path, file = sys.stderr)
                raise

        del self.caser
        del self.classifier

    
    def parse_vertical_format(self, soup_object):

        # If the element is not present, return empty list
        if soup_object is None:
            return []

        lines = soup_object.text.splitlines()
        lines = (line.strip() for line in lines)
        lines = filter(None, lines)
        return filter(None, map(VertItem, lines))

    def convert_to_tokens(self, iterable):  
        tokens = (self.caser(self.classifier(item)) for item in iterable)
        return tokens
        #return filter(lambda x: x not in config.stopwords, tokens)

    def bag_of_words(self, soup_object):
        verts = self.parse_vertical_format(soup_object)
        tokens = self.convert_to_tokens(verts) 
        return Counter(tokens)

    def section_length(self, tire):
        section = getattr(self, tire)
        return sum(section.values())


