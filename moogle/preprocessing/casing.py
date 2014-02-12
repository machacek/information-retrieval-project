from factory import Factory

caser_factory = Factory(init=False, types={
        'yes' : lambda x: x.lower(),
        'no' : lambda x: x,
    })
