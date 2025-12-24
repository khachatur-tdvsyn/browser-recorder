from abc import ABC, abstractmethod

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
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

    def __str__(self):
        return self.params

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.params}>"


class ClickAction(BaseAction):
    def execute(self):
        wait = WebDriverWait(self.driver, 10)
        el = wait.until(
            lambda driver: driver.find_element(
                by=By.CSS_SELECTOR, value=self.params["target"]
            )
        )

        print("Clicking on", self.params["target"])
        try:
            el.click()
        except ElementNotInteractableException:
            action = ActionChains(self.driver)
            action.move_to_element(el).click().perform()


class DoubleClickAction(BaseAction):
    def execute(self):
        wait = WebDriverWait(self.driver, 10)
        el = wait.until(
            lambda driver: driver.find_element(
                by=By.CSS_SELECTOR, value=self.params["target"]
            )
        )

        print("Double clicking on", self.params["target"])
        try:
            action = ActionChains(self.driver)
            action.double_click(el)
        except ElementNotInteractableException:
            action.move_to_element(el).double_click()
        finally:
            action.perform()


class MouseBaseAction(BaseAction):
    def __init__(self, driver, params):
        super().__init__(driver, params)
        self.html = self.driver.find_element(by=By.TAG_NAME, value="html")

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
        return self.driver.execute_script(
            """
            return window.__mousePos
                ? { x: window.__mousePos.x, y: window.__mousePos.y }
                : null;
        """
        )

    def _refresh_html_element(self):
        try:
            self.html.is_enabled()
        except StaleElementReferenceException:
            self.html = self.driver.find_element(by=By.TAG_NAME, value="html")

    def _create_move_action(self):
        action = ActionChains(self.driver)
        self._refresh_html_element()
        action.move_to_element_with_offset(
            self.html, self.normalized_x, self.normalized_y
        )
        return action


class MouseDownAction(MouseBaseAction):
    def execute(self):

        wait = WebDriverWait(self.driver, 10)
        wait.until(
            lambda d: d.find_element(by=By.CSS_SELECTOR, value=self.params["target"])
        )

        action = ActionChains(self.driver)
        print("Executing MouseDownAction on", self.params["target"])

        action = self._create_move_action()

        # Mouse button: 0 = left, 1 = middle, 2 = right
        button_type = self.params["event"].get("button", 0)
        if button_type == 2:
            action.context_click()
        else:
            action.click_and_hold()
        action.perform()
        print(self.get_mouse_position())


class MouseUpAction(MouseBaseAction):
    def execute(self):
        print(self.get_mouse_position())
        action = self._create_move_action()

        action.release()
        action.perform()

        print(self.get_mouse_position())


class MouseMoveAction(MouseBaseAction):
    def execute(self):
        print(
            "Executing MouseMoveAction at",
            self.params["event"]["clientX"],
            self.params["event"]["clientY"],
        )

        action = self._create_move_action()
        action.perform()
        print(self.get_mouse_position())


class WheelAction(BaseAction):
    def execute(self):
        print(
            "Executing WheelAction by",
            self.params["event"]["deltaY"],
        )

        action = ActionChains(self.driver)
        delta_y = self.params["event"].get("deltaY", 0)
        scroll_amount = int(delta_y)  # Adjust scroll sensitivity as needed
        action.scroll_by_amount(0, scroll_amount)
        action.perform()


class ActionFactory:
    avaiable_actions = {
        "onclick": ClickAction,
        "onmousedown": MouseDownAction,
        "onmouseup": MouseUpAction,
        "onmousemove": MouseMoveAction,
        "ondblclick": DoubleClickAction,
        "onwheel": WheelAction,
    }

    @classmethod
    def create_action(cls, driver, params) -> list[BaseAction]:
        action_objects = []
        for p in params:
            if cls.avaiable_actions.get(p.get("type")):
                action_objects.append(cls.avaiable_actions[p["type"]](driver, p))

        return action_objects
