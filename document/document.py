import os

from bs4 import BeautifulSoup

from .token import Token

class Document(object):
    """
    This class represents raw documents in vertical format.
    """

    def __init__(self, *path_parts):

        document_path = os.path.join(*path_parts)
        self.parse_vertical_format(document_path)
    
    def parse_vertical_format(self, document_path)
        with open(document_path, 'r') as file:
            soup = BeautifulSoup(file, "xml") 

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

    def parse_section(self, soup_object):

        # If the element is not present, return empty list
        if soup_object is None:
            return []

        lines = soup_object.text.splitlines()
        lines = (line.strip() for line in lines)
        lines = filter(None, lines)
        tokens = map(Token, lines)
        return list(tokens)
