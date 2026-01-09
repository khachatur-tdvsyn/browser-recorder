from enum import Enum
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService


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
    _avaiable_services = {
        BrowserType.CHROME: ChromeService,
        BrowserType.FIREFOX: FirefoxService,
        BrowserType.EDGE: EdgeService,
        BrowserType.SAFARI: SafariService
    }
    @classmethod
    def create(cls, browser: BrowserType, executable_path: Path | None = None, **kwargs) -> WebDriver:
        try:
            service_cls = cls._avaiable_services[browser]
            driver_cls = cls._avaiable_drivers[browser]
        except KeyError:
            raise ValueError(f"Unsupported browser: {browser}")

        service = service_cls(executable_path=executable_path)
        return driver_cls(service=service, **kwargs)