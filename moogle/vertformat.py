import os
from bs4 import BeautifulSoup

from config import config

class VertItem(object):
    def __init__(self, line):
        fields = line.split(sep='\t')

        if len(fields) != 6:
            raise ValueError("Line \"%s\" has %s fields" % (fields, len(fields)))
        
        self.order  = int(fields[0])
        self.form   = fields[1]
        self.lemma  = fields[2]
        self.tag    = fields[3]

        # We are not doing this now
        # self.parrent  = fields[4]
        # self.syn_type = fields[5]

class VertFormat(object):
    """
    """

    def __init__(self, path):
        with open(path, 'r') as file:
            soup = BeautifulSoup(file, "xml") 
            self.process_soup(soup)
    
    def parse_vertical_format(self, soup_object):

        # If the element is not present, return empty list
        if soup_object is None:
            return []

        lines = soup_object.text.splitlines()
        lines = (line.strip() for line in lines)
        lines = filter(None, lines)
        return map(VertItem, lines)

    def convert_to_tokens(self, iterable):  
        tokens = (config.case(config.classifier(item) for item in iterable)
        return filter(lambda x: x not in config.stopwords, tokens)

    def bag_of_words(self, soup_object):
        verts = self.parse_vertical_format(soup_object)
        tokens = self.convert_to_tokens(verts) 
        return Counter(tokens)

