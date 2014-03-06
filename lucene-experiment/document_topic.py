from __future__ import print_function

import sys
from bs4 import BeautifulSoup
from config import config
from vertitem import VertItem

class DocumentTopicBase(object):
    def __init__(self, path):
        with open(path, 'r') as file:
            try:
                soup = BeautifulSoup(file, "xml") 
                self.process_soup(soup)
            except ValueError:
                print("Error in file: %s" % path, file = sys.stderr)
                raise
    
    def converted_tokens_str(self, soup_list):
        " ".join(self.converted_tokens(soup_list))

    def converted_tokens(self, soup_list):
        for vert_item in self.vert_items(soup_list):
            yield config.lowercase(config.term(vert_item))

    def vert_items(self, soup_list):
        result = []
        for soup in soup_list:
            lines = soup.text.splitlines()
            lines = (line.strip() for line in lines)
            lines = filter(None, lines)
            result += list(filter(None, map(VertItem, lines)))
        return result

class Topic(DocumentTopicBase):
    
    def process_soup(self, soup):
        self.num = soup.top.num.text.strip()
        self.title = self.converted_tokens_str(soup.DOC.find_all("title"))
        self.desc = self.converted_tokens_str(soup.DOC.find_all("desc"))
        self.narr = self.converted_tokens_str(soup.DOC.find_all("narr"))

    def __repr__(self):
        return "<Topic %s: %s>" % (self.num, self.title)


class Document(DocumentTopicBase):
    def process_soup(self, soup):
        self.docid = soup.DOC.DOCID.text.strip()
        self.docno = soup.DOC.DOCNO.text.strip()
        self.date  = soup.DOC.DATE.text.strip()
        self.title = self.converted_tokens_str(soup.DOC.find_all("TITLE"))
        self.heading = self.converted_tokens_str(soup.DOC.find_all("HEADING"))
        self.text = self.converted_tokens_str(soup.DOC.find_all("TEXT"))

    def __repr__(self):
        return "<Document %s: %s>" % (self.docid, self.title)
