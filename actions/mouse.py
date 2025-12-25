from .base import BaseAction, MouseBaseAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException

from js_utils import DRAG_DROP_PAYLOAD

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

class DragAction(BaseAction):
    def execute(self):
        ...

class DropAction(BaseAction):
    def __init__(self, driver, params):
        super().__init__(driver, params)
        self.driver.execute_script(DRAG_DROP_PAYLOAD)

    def execute(self):
        wait = WebDriverWait(self.driver, 10)
        el = wait.until(
            lambda driver: driver.find_element(
                by=By.CSS_SELECTOR, value=self.params[0]["target"]
            )
        )

        wait = WebDriverWait(self.driver, 10)
        next_el = wait.until(
            lambda driver: driver.find_element(
                by=By.CSS_SELECTOR, value=self.params[1]["target"]
            )
        )

        print("Dragging element", self.params[0]["target"])
        print("Dropping on element", self.params[1]["target"])
        action = ActionChains(self.driver)
        action.drag_and_drop(el, next_el).perform()

        # self.driver.execute_script(
        #     "window.__html5DragAndDrop(arguments[0], arguments[1]);", el, next_el
        # )

        