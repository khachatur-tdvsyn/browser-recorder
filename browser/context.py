from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from logging import getLogger
logger = getLogger(__name__)

class FrameContextDriver:
    def __init__(self, driver: WebDriver, iframes_selector: list[str]):
        self.driver = driver
        self.iframes_selector = iframes_selector

    def __enter__(self):
        logger.debug(f'Switching to iframes {self.iframes_selector}')
        for i in self.iframes_selector:
            iframe = self.driver.find_element(By.CSS_SELECTOR, i)
            self.driver.switch_to.frame(iframe)
    
    def __exit__(self, exc_type, exc_val, tb):
        logger.debug(f'Switch back from iframes {exc_type}, {exc_val}, {tb}')
        self.driver.switch_to.default_content()
