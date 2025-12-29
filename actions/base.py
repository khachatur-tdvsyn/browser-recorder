from abc import ABC, abstractmethod

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    MoveTargetOutOfBoundsException
)
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from recorder.recorder import BoundaryRecorder
from browser.context import FrameContextDriver

from logging import getLogger

logger = getLogger(__name__)

class BaseAction(ABC):
    def __init__(self, driver: WebDriver, params: dict):
        super().__init__()
        self.driver = driver
        self.params = params
        
        self.frame_context = FrameContextDriver(self.driver, self.params.get('parentIframes'))

    @abstractmethod
    def execute(self): ...

    def _get_element(self, target, timeout=10) -> WebElement:
        with self.frame_context:
            logger.debug(f'Find element {target=} - parent iframes {self.params.get("parentIframes")[-1:]}')
            wait = WebDriverWait(self.driver, timeout)
            el = wait.until(
                lambda d: d.find_element(
                    by=By.CSS_SELECTOR, value=target
                )
            )
            logger.debug(f'Found element:", {target=} - parent iframes {self.params.get("parentIframes")[-1:]}')

        return el

    def __str__(self):
        return self.params

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.params}>"


class UnknownAction(BaseAction):
    def execute(self):
        logger.warning(f"Executing unknown action of type: {self.params['type']} (doing nothing)")

class MouseBaseAction(BaseAction, ABC):
    def __init__(self, driver, params, boundary_recorder: BoundaryRecorder):
        super().__init__(driver, params)
        self.boundary_recorder = boundary_recorder

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

    def get_mouse_position(self):
        return self.driver.execute_script("""return window.__mousePos""")

    def _create_move_action(self):
        action = ActionChains(self.driver)
        action.w3c_actions.pointer_action.move_to_location(x = self.params['event']['clientX'], y = self.params['event']['clientY'])
        return action
    
    def execute(self):
        ...