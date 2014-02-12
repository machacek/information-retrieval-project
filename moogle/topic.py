from vertformat import VertFormat

class Topic(VertFormat):
    """
    """
    
    def process_soup(self, soup):
        # These shoud be present for sure
        self.num = soup.top.num.text.strip()

        # Parse the sections
        self.title = self.bag_of_words(soup.top.title)
        self.desc = self.bag_of_words(soup.top.desc)
        self.narr = self.bag_of_words(soup.top.narr)

    def __repr__(self):
        return "<Topic: %s>" % self.num
