import json
from logging import getLogger

from .base import BaseEventStorage
from recorder.shortener import (
    ClickActionsShortener,
    ClipboardActionsShortener,
    WheelActionsShortener,
    MouseMoveLinearShortener
)

logger = getLogger(__name__)

class JSONEventStorage(BaseEventStorage):
    def load(self, path):
        try:
            logger.info(f'Loading events from {path}')
            with open(path) as f:
                self.records = json.load(f)
            logger.info(f'Events loaded successfully {len(self.records)}')
        except Exception as e:
            logger.error("Unable to load records", exc_info=e)

    
    def _shorten(self):
        for Shortener in (ClickActionsShortener, WheelActionsShortener, MouseMoveLinearShortener, ClipboardActionsShortener):
            logger.debug(f'Shorten by {Shortener.__name__}')
            self.records = Shortener(self.records).shorten()


    def save(self, path):
        try:
            logger.debug(f'Saving new records to {path}')
            self._shorten()
            with open(path, 'w') as f:
                json.dump(self.records, f) 
            logger.debug('Saved successfully.')
        except Exception as e:
            logger.error('Unable to save records', exc_info=e)