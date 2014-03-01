from __future__ import print_function

import sys
from bs4 import BeautifulSoup

class DocumentTopicBase(object):
    def __init__(self, path):
        with open(path, 'r') as file:
            try:
                soup = BeautifulSoup(file, "xml") 
                self.process_soup(soup)
            except ValueError:
                print("Error in file: %s" % path, file = sys.stderr)
                raise

def text(soup_object):
    try:
        return soup_object.text
    except AttributeError:
        return ""



class Topic(DocumentTopicBase):
    
    def process_soup(self, soup):
        self.num = soup.top.num.text.strip()
        self.title = text(soup.top.title)
        self.desc = text(soup.top.desc)
        self.narr = text(soup.top.narr)

    def __repr__(self):
        return "<Topic: %s>" % self.num



class Document(DocumentTopicBase):
    def process_soup(self, soup):
        self.docid = text(soup.DOC.DOCID)
        self.docno = text(soup.DOC.DOCNO)
        self.date  = text(soup.DOC.DATE)
        self.title = text(soup.DOC.TITLE)
        self.heading = text(soup.DOC.HEADING)
        self.text = text(soup.DOC.TEXT)

    def __repr__(self):
        return "<Document: %s>" % self.docid
