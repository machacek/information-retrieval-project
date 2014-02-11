import os
from collections import Counter

from bs4 import BeautifulSoup

from vert import VertFormat

class TopicVert(VertFormat):
    """
    This class represents raw topics in vertical format.
    """
    
    def process_soup(self, soup):
        # These shoud be present for sure
        self.num = soup.top.num.text.strip()

        # Parse the sections
        self.title = self.parse_section(soup.top.title)
        self.desc = self.parse_section(soup.top.desc)
        self.narr = self.parse_section(soup.top.narr)

    def __repr__(self):
        return "<Topic: %s>" % self.num

class TopicTokens(object):
    """
    This class represents topics converted from vertical format to list of tokens representation
    """

    def __init__(self, topic_vert, classifier):
        self.num = topic_vert.num
        self.title = classifier.convert_vert_list(topic_vert.title)
        self.desc = classifier.convert_vert_list(topic_vert.desc)
        self.narr = classifier.convert_vert_list(topic_vert.narr)

class TopicBag(object):
    """
    This class representes topics as a bag of terms
    """

    def __init__(self, topic_tokens):
        self.num = topic_tokens.num
        self.title = Counter(topic_tokens.title)
        self.desc = Counter(topic_tokens.desc)
        self.narr = Counter(topic_tokens.narr)


