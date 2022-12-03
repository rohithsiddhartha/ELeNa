
from abc import abstractmethod
from src import *
from abc import ABC, abstractmethod
from src.model import observable

class Observer:

    @abstractmethod
    def update(self, observable):
        pass