import json

from .base import BaseEventStorage
from recorder.shortener import (
    ClickActionsShortener,
    ClipboardActionsShortener,
    WheelActionsShortener,
    MouseMoveLinearShortener
)

class JSONEventStorage(BaseEventStorage):
    def load(self, path):
        with open(path) as f:
            self.records = json.load(f)
    
    def _shorten(self):
        for Shortener in (ClickActionsShortener, WheelActionsShortener, MouseMoveLinearShortener, ClipboardActionsShortener):
            print('Shorten by', Shortener.__name__)
            self.records = Shortener(self.records).shorten()


    def save(self, path):
        self._shorten()
        with open(path, 'w') as f:
            json.dump(self.records, f) 