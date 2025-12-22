import json

from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BaseAction(ABC):
    def __init__(self, driver: WebDriver, params: dict):
        super().__init__()
        self.driver = driver
        self.params = params
    
    @abstractmethod
    def execute(self):
        ...
    
    def __str__(self):
        return self.params

class ClickAction(BaseAction):
    def execute(self):
        el = self.driver.find_element(by=By.CSS_SELECTOR, value=self.params['target'])
        el.click()

class ActionFactory:
    avaiable_actions = {
        'onclick': ClickAction
    }

    @classmethod
    def create_action(cls, driver, params) -> list[BaseAction]:
        action_objects = []
        for p in params:
            if cls.avaiable_actions.get(p.get('type')):
                action_objects.append(
                    cls.avaiable_actions[p['type']](driver, p)
                )
        
        return action_objects