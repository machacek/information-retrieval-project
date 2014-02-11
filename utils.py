class Factory(object):
    def __init__(self, types):
        self.types = types
        
    def choices(self):
        return self.types.keys() 

    def __call__(self, type_str):
        type_name, config_str = type_str.split(':',2)
        args = config_str.split(',')
        return self.types[type_name](*args)
