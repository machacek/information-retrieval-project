from utils import Factory

caser_factory = Factory({
        'yes' : lambda x: x.lower(),
        'no' : lambda x: x,
    })
