
from src.model import *

class Observable:

    def __init__(self):
        self.isStateChange = False 
        self.observers = set() 

    def register(self, obs):
        self.observers.add(obs)
    
    def unegister(self, obs):
        self.observers.remove(obs)

    def state_changed(self):
        pass
    
    def get_state(self):
        return self.isStateChange

    def set_state(self, state):
        self.isStateChange = state
