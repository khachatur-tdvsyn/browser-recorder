from .base import BaseAction
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class CutAction(BaseAction):
    def execute(self):
        target_selector = self.params['target']
        print(f"Cutting text from {target_selector}")

        action = ActionChains(self.driver)
        action.key_down(Keys.CONTROL)
        action.send_keys('x')
        action.key_up(Keys.CONTROL)
        action.perform()  # Cut the text

class CopyAction(BaseAction):
    def execute(self):
        target_selector = self.params['target']
        print(f"Copying text from {target_selector}")
        
        action = ActionChains(self.driver)
        action.key_down(Keys.LEFT_CONTROL)
        action.send_keys('c')
        action.key_up(Keys.LEFT_CONTROL)
        action.perform()  # Copy the text

class PasteAction(BaseAction):
    def execute(self):
        clipboard_text = self.driver.execute_script("return navigator.clipboard.readText();")
        target_selector = self.params['target']
        print(f"Pasting text into {target_selector}: {clipboard_text}")
        target_element = self.driver.find_element(by=By.CSS_SELECTOR, value=target_selector)
        target_element.send_keys(clipboard_text)