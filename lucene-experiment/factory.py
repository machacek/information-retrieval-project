import argparse

class Factory(object):
    def __init__(self, types, init=True):
        self.types = types
        self.init = init
        
    def choices(self):
        return self.types.keys() 

    def metavar(self):
        return "{" + ",".join(self.choices()) + "}"

    def __call__(self, type_str):
        try:
            if ':' in type_str:
                type_name, config_str = type_str.split(':',2)
                args = config_str.split(',')
                if self.init:
                    return self.types[type_name](*args)
                else:
                    return self.types[type_name]
            else:
                type_name = type_str
                if self.init:
                    return self.types[type_name]()
                else:
                    return self.types[type_name]
        except:
            raise argparse.ArgumentTypeError("'%s' is invalid argument." % type_str)
