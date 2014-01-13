from .stopper import Stopper

class NoStopper(Stopper):
    def stop(self, str):
        return False
