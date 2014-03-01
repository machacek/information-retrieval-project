class VertItem(object):
    def __init__(self, line):
        self.valid = True
        fields = line.split(sep='\t')

        if len(fields) != 6:
            warnings.warn("Line \"%s\" has %s fields" % (line, len(fields)))
            self.valid = False
            return
        
        self.order  = int(fields[0])
        self.form   = fields[1]
        self.lemma  = fields[2]
        self.tag    = fields[3]

        # We are not doing this now
        # self.parrent  = fields[4]
        # self.syn_type = fields[5]

    def __bool__(self):
        return self.valid
