from utils import Factory

from .nostopper import NoStopper

stopper_factory = Factory({
    'none' : NoStopper,
    })

