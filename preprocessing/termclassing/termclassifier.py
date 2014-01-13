class TermClassifier(object):
    def convert_iterable(self, iterable):
        return [self.convert_str(token) for token in iterable]
