from utils import Factory

class Caser(object):
    def case_iterable(iterable):
        return map(self.case_str, iterable)

class LowerCaser(Caser):
    def case_str(str):
        return str.lower()

class OriginalCaser(Caser):
    def case_str(str):
        return str

lowercaser_factory = Factory({
        'yes' : LowerCaser,
        'no' : OriginalCaser,
    })
