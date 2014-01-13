class Factory(object):
    def __init__(self, types):
        self.types = types
        
    def choices(self):
        return self.types.keys() 

    def __call__(self, type_name, *args, **kwargs):
        return self.types[type_name](*args, **kwargs)
