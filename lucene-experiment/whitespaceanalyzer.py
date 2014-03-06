import lucene

class WhitespaceAnalyzer(lucene.PythonAnalyzer):
    def tokenStream(self, fieldName, reader):
        return lucene.WhitespaceTokenizer(reader)
