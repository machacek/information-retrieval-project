class VertItem(object):
    def __init__(self, line):
        self.valid = True
        fields = line.split('\t')

        if len(fields) != 6:
            self.valid = False
            return

        self.form   = fields[1]
        self.lemma  = fields[2]
        self.tag    = fields[3]

    def __bool__(self):
        return self.valid

    def __unicode__(self):
        return u"<VertItem form: %s, lemma: %s, tag: %s>" %(self.form, self.lemma, self.tag)
