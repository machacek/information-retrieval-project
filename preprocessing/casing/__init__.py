from utils import Factory

class Caser(object):
    def case_iterable(self, iterable):
        return [self.case_str(token) for token in iterable]

class LowerCaser(Caser):
    def case_str(self, str):
        return str.lower()

class OriginalCaser(Caser):
    def case_str(self, str):
        return str

lowercaser_factory = Factory({
        'yes' : LowerCaser,
        'no' : OriginalCaser,
    })
