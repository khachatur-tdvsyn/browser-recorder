from abc import ABC, abstractmethod
from typing import Iterable

class BaseEventStorage(ABC):
    def __init__(self):
        self.records = []
    
    @abstractmethod
    def load(self, path):
        ...

    def add_event(self, item: dict):
        self.records.append(item)
    
    def add_many_events(self, items: Iterable):
        self.records.extend(items)

    @abstractmethod
    def save(self, path):
        ...
    