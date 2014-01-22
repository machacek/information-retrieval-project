import os

from bs4 import BeautifulSoup

from verttoken import VerticalFormat

class Document(VerticalFormat):
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
