import os

from bs4 import BeautifulSoup

from verttoken import VerticalFormat

class Topic(VerticalFormat):
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
