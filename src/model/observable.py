
from src.model import *

class Observable:
    """Class for all methods of an observable"""

    def __init__(self):

        self.isStateChange = False 
        self.observers = set() 

    def register(self, obs):
        """Register an observer"""
        self.observers.add(obs)
    
    def unegister(self, obs):
        """Unregister a registered observer"""
        self.observers.remove(obs)

    def state_changed(self):
        """Notify all observers when a state is changed"""
        pass
    
    def get_state(self):
        """Get the current state"""
        return self.isStateChange

    def set_state(self, state):
        """Set the current state to true"""
        self.isStateChange = state
