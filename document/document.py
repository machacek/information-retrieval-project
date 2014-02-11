import os

from bs4 import BeautifulSoup

from vert import VertFormat

class DocumentVert(VertFormat):
    """
    This class represents raw documents in vertical format.
    """

    def process_soup(self, soup):
        # These shoud be present for sure
        self.docid = soup.DOC.DOCID.text
        self.docno = soup.DOC.DOCNO.text
        self.date  = soup.DOC.DATE.text

        # Geography might not be present
        try:
            self.geography = soup.DOC.GEOGRAPHY.text
        except:
            self.geography = None

        # Parse the sections
        self.title = self.parse_section(soup.DOC.TITLE)
        self.heading = self.parse_section(soup.DOC.HEADING)
        self.text = self.parse_section(soup.DOC.TEXT)

    def __repr__(self):
        return "<Document: %s>" % self.docid

class DocumentTokens(object):
    """ 
    This class represents documents converted from vertical format to list of tokens representation
    """

    def __init__(self, document_vert, classifier):
        self.docid, self.docno, self.date = document_vert.docid, document_vert.docno, document_vert.date
        self.title = classifier.convert_vert_list(document_vert.title)
        self.heading = classifier.convert_vert_list(document_vert.heading)
        self.text = classifier.convert_vert_list(document_vert.text)

class DocumentBag(object):
    """
    This class representes documents as a bag of terms
    """

    def __init__(self, document_tokens):
        self.docid, self.docno, self.date = document_tokens.docid, document_tokens.docno, document_tokens.date
        self.title = Counter(document_tokens.title)
        self.heading = Counter(document_tokens.heading)
        self.text = Counter(document_tokens.text)

