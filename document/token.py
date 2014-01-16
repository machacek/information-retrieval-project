

class Token(object):
    def __init__(self, line):

        fields = line.split(sep='\t')

        if len(fields) != 6:
            raise ValueError("Line \"%s\" does has %s fields" % (fields, len(fields)))
        
        self.order  = int(fields[0])
        self.form   = fields[1]
        self.lemma  = fields[2]
        self.tag    = fields[3]

        # We are not doing this now
        # self.parrent  = fields[4]
        # self.syn_type = fields[5]

