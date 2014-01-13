class Stopper(object):
    def filter_out(self, iterable):
        return [token for token in iterable if not self.stop(token)]


