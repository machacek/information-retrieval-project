import os

from bs4 import BeautifulSoup

from .vertitem import VertItem

class VerticalFormat(object):
    """
    This class represents base class, that that represents
    vertical format files. All you need to do is to implement
    process_soup method.
    """

    def __init__(self, *path_parts):
        path = os.path.join(*path_parts)
        with open(path, 'r') as file:
            soup = BeautifulSoup(file, "xml") 
            self.process_soup(soup)
    
    def parse_section(self, soup_object):

        # If the element is not present, return empty list
        if soup_object is None:
            return []

        lines = soup_object.text.splitlines()
        lines = (line.strip() for line in lines)
        lines = filter(None, lines)
        tokens = map(VertItem, lines)
        return list(tokens)
