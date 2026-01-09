from enum import Enum

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class BrowserType(Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    EDGE = "edge"
    SAFARI = "safari"


class WebDriverFactory:
    _avaiable_drivers = {
        BrowserType.CHROME: webdriver.Chrome,
        BrowserType.FIREFOX: webdriver.Firefox,
        BrowserType.EDGE: webdriver.Edge,
        BrowserType.SAFARI: webdriver.Safari,
    }
    @classmethod
    def create(cls, browser: BrowserType, **kwargs) -> WebDriver:
        try:
            driver_cls = cls._avaiable_drivers[browser]
        except KeyError:
            raise ValueError(f"Unsupported browser: {browser}")

        return driver_cls(**kwargs)