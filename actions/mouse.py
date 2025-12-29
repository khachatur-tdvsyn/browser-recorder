import time

from .base import BaseAction, MouseBaseAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException

from js_utils import DRAG_DROP_PAYLOAD
from logging import getLogger

logger = getLogger(__name__)

class ClickAction(BaseAction):
    def execute(self):
        el = self._get_element(self.params["target"])

        with self.frame_context:
            logger.debug(f'Clicking on self.params["target"]')
            try:
                el.click()
            except ElementNotInteractableException:
                action = ActionChains(self.driver)
                action.move_to_element(el).click().perform()
            


class DoubleClickAction(BaseAction):
    def execute(self):
        el = self._get_element(self.params["target"])

        with self.frame_context:
            logger.debug(f'Double clicking on {self.params["target"]}')
            try:
                action = ActionChains(self.driver)
                action.double_click(el)
            except ElementNotInteractableException:
                action.move_to_element(el).double_click()
            finally:
                action.perform()

class MouseDownAction(MouseBaseAction):
    def execute(self):
        super().execute()
        logger.debug(f'Executing MouseDownAction on {self.params["target"]}')
        with self.frame_context:
            action = self._create_move_action()
            logger.debug(self.get_mouse_position())
            # Mouse button: 0 = left, 1 = middle, 2 = right
            button_type = self.params["event"].get("button", 0)
            if button_type == 2:
                action.context_click()
            else:
                action.click_and_hold()
            action.perform()
            logger.debug(self.get_mouse_position())


class MouseUpAction(MouseBaseAction):
    def execute(self):
        super().execute()
        with self.frame_context:
            logger.debug(f'Executing MouseUpAction on {self.params["target"]}')
            action = self._create_move_action()

            action.release()
            action.perform()
        
        logger.debug(self.get_mouse_position())


class MouseMoveAction(MouseBaseAction):
    def _get_position(self, start, end, theresold):
        return (end-start) * theresold + start

    def _slow_execute(self):
        startX, startY = (
            self.params['event']['startClientX'], 
            self.params['event']['startClientY'],
        )
        endX, endY = (
            self.params['event']['clientX'], 
            self.params['event']['clientY'],
        )
        duration = self.params.get('duration', 40)
        theresold = 0

        # Interval in milliseconds
        interval = 50
        while theresold <= 1:
            t = time.time()
            action = ActionChains(self.driver)

            currX, currY = self._get_position(startX, endX, theresold), self._get_position(startY, endY, theresold)
            #print('Moving to', currX, currY, 'with theresold', theresold)
            action.move_to_element_with_offset(
                self.boundary_recorder.html,
                int(currX),
                int(currY)
            )
            action.perform()
            delta = int((time.time() - t) * 1000)
            theresold += (interval + delta) / duration
            time.sleep(max(interval - delta, 0) / 1000)

    def execute(self):
        super().execute()
        with self.frame_context:
            logger.debug(
                f'Executing MouseMoveAction at \
                {self.params["event"]["clientX"]} \
                 {self.params["event"]["clientY"]}'
            )
            self._slow_execute()


class WheelAction(BaseAction):
    def _slow_execute(self):
        delta_y = self.params["event"].get("deltaY", 0)
        duration = self.params.get('duration', 40)

        # Interval in milliseconds
        scrolled_delta, interval = 0, 40
        scroll_amount = delta_y / (duration / interval)
        logger.debug(f'{scroll_amount=} {int(scroll_amount)}')
        while abs(scrolled_delta) < abs(delta_y):
            action = ActionChains(self.driver)
            action.scroll_by_amount(0, int(scroll_amount))
            action.perform()
            scrolled_delta += scroll_amount
            time.sleep(interval / 1000)

    def execute(self):
        logger.debug(
            f'Executing WheelAction by \
            {self.params["event"]["deltaY"]}',
        )

        self._slow_execute()

class DragAction(BaseAction):
    def execute(self):
        ...

class DropAction(BaseAction):
    def __init__(self, driver, params):
        super().__init__(driver, params)
        self.driver.execute_script(DRAG_DROP_PAYLOAD)

    def execute(self):
        el = self._get_element(self.params[0]["target"])
        next_el = self._get_element(self.params[1]["target"])

        action = ActionChains(self.driver)
        action.drag_and_drop(el, next_el).perform()

        # self.driver.execute_script(
        #     "window.__html5DragAndDrop(arguments[0], arguments[1]);", el, next_el
        # )

        