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




class Topic(DocumentTopicBase):
    
    def process_soup(self, soup):
        self.num = soup.top.num.text.strip()
        self.title = "\n".join([x.text for x in soup.DOC.find_all("title")])
        self.desc = "\n".join([x.text for x in soup.DOC.find_all("desc")])
        self.narr = "\n".join([x.text for x in soup.DOC.find_all("narr")])

    def __repr__(self):
        return "<Topic: %s>" % self.num


class Document(DocumentTopicBase):
    def process_soup(self, soup):
        self.docid = soup.DOC.DOCID.text.strip()
        self.docno = soup.DOC.DOCNO.text.strip()
        self.date  = soup.DOC.DATE.text.strip()
        self.title = "\n".join([x.text for x in soup.DOC.find_all("TITLE")])
        self.heading = "\n".join([x.text for x in soup.DOC.find_all("HEADING")])
        self.text = "\n".join([x.text for x in soup.DOC.find_all("TEXT")])

    def __repr__(self):
        return "<Document: %s>" % self.docid
