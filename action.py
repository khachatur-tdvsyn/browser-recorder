from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class BaseAction(ABC):
    def __init__(self, driver: WebDriver, params: dict):
        super().__init__()
        self.driver = driver
        self.params = params

    @abstractmethod
    def execute(self): ...

    def __str__(self):
        return self.params


class ClickAction(BaseAction):
    def execute(self):
        el = self.driver.find_element(by=By.CSS_SELECTOR, value=self.params["target"])
        el.click()


class MouseBaseAction(BaseAction):
    def __init__(self, driver, params):
        super().__init__(driver, params)
        self.html = self.driver.find_element(by=By.TAG_NAME, value="html")

        # Temporary install mouse tracker
        self.driver.execute_script("""
        (function () {
            if (window.__mouseTrackerInstalled) return;
            window.__mouseTrackerInstalled = true;

            window.__mousePos = { x: null, y: null };

            document.addEventListener("mousemove", function (e) {
                window.__mousePos.x = e.clientX;
                window.__mousePos.y = e.clientY;
            }, true);
        })();
        """)
        self.boundaries = self.driver.execute_script("""return {x: window.innerWidth, y: window.innerHeight};""")
        self.normalized_x, self.normalized_y = (
            self.params["event"]["clientX"] - self.boundaries["x"] / 2,
            self.params["event"]["clientY"] - self.boundaries["y"] / 2,
        )

    def get_mouse_position(self):
        return self.driver.execute_script("""
            return window.__mousePos
                ? { x: window.__mousePos.x, y: window.__mousePos.y }
                : null;
        """)

class MouseDownAction(MouseBaseAction):
    def execute(self):
        action = ActionChains(self.driver)
        print(
            "Executing MouseDownAction at",
            self.params["event"]["clientX"],
            self.params["event"]["clientY"],
        )

        print(self.get_mouse_position())
        action.move_to_element_with_offset(
            self.html, self.normalized_x, self.normalized_y
        )

        # Mouse button: 0 = left, 1 = middle, 2 = right
        button_type = self.params["event"].get("button", 0)
        if(button_type == 2):
            action.context_click()
        else:
            action.click_and_hold()
        action.perform()
        print(self.get_mouse_position())


class MouseUpAction(MouseBaseAction):
    def execute(self):
        action = ActionChains(self.driver)
        print(
            "Executing MouseUpAction at",
            self.params["event"]["clientX"],
            self.params["event"]["clientY"],
        )

        el = self.driver.find_element(by=By.CSS_SELECTOR, value=self.params["target"])

        print(self.get_mouse_position())
        action.move_to_element_with_offset(
            self.html, self.normalized_x, self.normalized_y
        )
        action.release()
        action.perform()
        print(self.get_mouse_position())


class ActionFactory:
    avaiable_actions = {
        "onclick": ClickAction,
        "onmousedown": MouseDownAction,
        "onmouseup": MouseUpAction,
    }

    @classmethod
    def create_action(cls, driver, params) -> list[BaseAction]:
        action_objects = []
        for p in params:
            if cls.avaiable_actions.get(p.get("type")):
                action_objects.append(cls.avaiable_actions[p["type"]](driver, p))

        return action_objects
