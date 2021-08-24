from dependencies import *
import numpy as np

class BaseState:
    def __init__(self):
        pass

    def update(self, state_machine, mouse, click):
        pass

    def enter(self, params=None):
        pass

    def exit(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__
