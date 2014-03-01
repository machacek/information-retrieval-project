import lucene

from config import config
from vertitem import VertItem

class NewLineTokenizer(lucene.PythonCharTokenizer):
    def __init__(self, reader):
        super(NewLineTokenizer, self).__init__(reader)

    def isTokenChar(self, c):
        return c != "\n"

class TransformBase(lucene.PythonTokenFilter):
    def __init__(self, input):
        super(TransformBase, self).__init__(input)
        self.termAtt = self.addAttribute(lucene.CharTermAttribute.class_)
        self.input = input

    def incrementToken(self):
        if self.input.incrementToken():
            string = self.termAtt.toString()
            string = self.transform(string)
            self.termAtt.setEmpty()
            self.termAtt.append(string)
            return True
        return False

class FilterBase(lucene.PythonTokenFilter):
    def __init__(self, input):
        super(FilterBase, self).__init__(input)
        self.termAtt = self.addAttribute(lucene.CharTermAttribute.class_)
        self.input = input

    def incrementToken(self):
        while self.input.incrementToken():
            string = self.termAtt.toString()
            if self.accept(string):
                return True
        return False

class StripLineTransform(TransformBase):
    def transform(self, string):
        return string.strip()

class NonEmptyLineFilter(FilterBase):
    def accept(self, string):
        return len(string) > 0

class TermClassFilter(TransformBase):
    def transform(self, string):
        vert_item = VertItem(string)
        return config.classes(vert_item)

class VertFormatAnalyzer(lucene.PythonAnalyzer):
    def tokenStream(self, fieldName, reader):
        lines = NewLineTokenizer(reader)
        lines = StripLineTransform(lines)
        return lines
        lines = NonEmptyLineFilter(lines)
        classes = TermClassFilter(lines)

        if config.lowercase:
            return lucene.LowerCaseFilter(classes)
        else:
            return classes
