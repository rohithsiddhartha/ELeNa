
from abc import abstractmethod
from src import *
from abc import ABC, abstractmethod
from src.model import observable

class Observer:

    """Update method for when the current state changes."""
    @abstractmethod
    def update(self, observable):
        pass