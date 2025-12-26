from abc import ABC, abstractmethod

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException
)


class BaseAction(ABC):
    def __init__(self, driver: WebDriver, params: dict):
        super().__init__()
        self.driver = driver
        self.params = params

    @abstractmethod
    def execute(self): ...

    def _get_element(self, target, timeout=10) -> WebElement:
        wait = WebDriverWait(self.driver, timeout)
        el = wait.until(
            lambda d: d.find_element(
                by=By.CSS_SELECTOR, value=target
            )
        )
        print("Found element:", target, self.params.get("parentIframes")[-1:])
        return el

    def __str__(self):
        return self.params

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.params}>"


class UnknownAction(BaseAction):
    def execute(self):
        print(f"Executing unknown action of type: {self.params['type']} (doing nothing)")

class MouseBaseAction(BaseAction, ABC):
    def __init__(self, driver, params):
        super().__init__(driver, params)
        self.html = self._get_element("html")

        # Temporary install mouse tracker
        self.driver.execute_script(
            """
        (function () {
            if (window.__mouseTrackerInstalled) return;
            window.__mouseTrackerInstalled = true;

            window.__mousePos = { x: null, y: null };

            document.addEventListener("mousemove", function (e) {
                window.__mousePos.x = e.clientX;
                window.__mousePos.y = e.clientY;
            }, true);
        })();
        """
        )
        self.boundaries = self.driver.execute_script(
            """return {x: window.innerWidth, y: window.innerHeight};"""
        )
        self.normalized_x, self.normalized_y = (
            self.params["event"]["clientX"] - self.boundaries["x"] / 2,
            self.params["event"]["clientY"] - self.boundaries["y"] / 2,
        )

    def get_mouse_position(self):
        return self.driver.execute_script("""return window.__mousePos""")

    def _refresh_html_element(self):
        try:
            self.html.is_enabled()
        except StaleElementReferenceException:
            self.html = self._get_element('html')

    def _create_move_action(self):
        action = ActionChains(self.driver)
        self._refresh_html_element()
        action.move_to_element_with_offset(
            self.html, self.normalized_x, self.normalized_y
        )
        return action