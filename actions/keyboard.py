from .base import BaseAction, UnknownAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class KeyboardBaseAction(BaseAction):
    @classmethod
    def _is_special_key(cls, key: str) -> bool:
        return key.upper() in Keys.__dict__.keys()
    
    @classmethod
    def _get_special_key(cls, key: str):
        return getattr(Keys, key.upper(), None)

class KeyDownAction(KeyboardBaseAction):
    def execute(self):
        key = self.params['event']['key']
        action = ActionChains(self.driver)
        if self._is_special_key(key):
            action.key_down(self._get_special_key(key))
        else:
            action.send_keys(key)
        action.perform()

class KeyUpAction(KeyboardBaseAction):
    def execute(self):
        key = self.params['event']['key']
        action = ActionChains(self.driver)
        if self._is_special_key(key):
            action.key_up(self._get_special_key(key)).perform()