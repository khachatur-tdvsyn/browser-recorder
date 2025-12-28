from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class FrameContextDriver:
    def __init__(self, driver: WebDriver, iframes_selector: list[str]):
        self.driver = driver
        self.iframes_selector = iframes_selector

    def __enter__(self):
        print('Switching to iframes', self.iframes_selector)
        for i in self.iframes_selector:
            iframe = self.driver.find_element(By.CSS_SELECTOR, i)
            self.driver.switch_to.frame(iframe)
    
    def __exit__(self, exc_type, exc_val, tb):
        print('Switch back from iframes', exc_type, exc_val, tb)
        self.driver.switch_to.default_content()
