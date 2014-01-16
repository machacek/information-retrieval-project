import os
import re

from textwrap import dedent

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

            # Strip the lines and filter out empty lines
            f = filter(None, (line.strip() for line in file)))

            opening_tag = "<DOC>"
            closing_tag = "</DOC>"

            # Initial <DOC> tag
            if next(f) != opening_tag:
                raise MalformedVerticalFormatException("Missing <DOC> tag at the first line")

            self.docid = self.parse_tag(f, "DOCID")
            self.docno = self.parse_tag(f, "DOCNO")
            self.date = self.parse_tag(f, "DATE")
            self.geography = self.parse_tag(f, "GEOGRAPHY")

            self.title = self.parse_section(f, "TITLE")
            self.heading = self.parse_section(f, "HEADING")
            self.text = self.parse_section(f, "TEXT")

            # Closing </DOC> tag
            if next(f) != closing_tag:
                raise MalformedVerticalFormatException("Expected </DOC> tag")

    # Compile the regular expresison once
    tag_re = re.compile(r"^<%s>(?P<value>.+)</%s>$" % tag)

    def parse_tag(self, f, tag):
        
        line = next(f)
        result = self.tag_re.match(line)
        if result is not None:
            return result.group('value')
        else:
            raise MalformedVerticalFormatException(
                    "The line \"\" does not match one line element format"
                    )

    def parse_section(self, f, section):     
        opening_tag = "<%s>" % section
        closing_tag = "</%s>" % section

        if next(f) != opening_tag:
            raise MalformedVerticalFormatException("Expected opening tag %s" % opening_tag)

        result = []

        for line in iter(f, closing_tag):
            result.append(Token(line))

        return result

    def __str__(self):
        return dedent("""
            DocID:      {docid} 
            DocNo:      {docno}
            date:       {date}
            geography:  {geography}

            title:
                {title1}
                {title2}
                ...




            """.format(
                docid = self.docid,
                docno = self.docno,
                date = self.date,
                geography = self.geography,
            )
    




    class MalformedVerticalFormatException(Exception):
        pass

