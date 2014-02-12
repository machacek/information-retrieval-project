from vertformat import VertFormat

class Document(VertFormat):
    """
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
        self.title = self.bag_of_words(soup.DOC.TITLE)
        self.heading = self.bag_of_words(soup.DOC.HEADING)
        self.text = self.bag_of_words(soup.DOC.TEXT)

    def __repr__(self):
        return "<Document: %s>" % self.docid
