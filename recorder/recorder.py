from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from browser.context import FrameContextDriver

class BoundaryRecorder:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.html_selector = None
        self.html = None
        self.saved_boundaries = {}
        self._is_into_iframe = False
        self._current_url = None

    def _insert_mousemove_event_recorder(self):
        self.driver.execute_script(
            """
        (function () {
            if (window.__mouseTrackerInstalled) return;
            window.__mouseTrackerInstalled = true;

            /*function toTopClient(e) {
                let x = e.clientX;
                let y = e.clientY;
                let win = window;

                while (win.frameElement) {
                    const rect = win.frameElement.getBoundingClientRect();
                    x += rect.left;
                    y += rect.top;
                    win = win.parent;
                }
                return { x, y };
            }*/

            window.__mousePos = { x: null, y: null };

            document.addEventListener("mousemove", function (e) {
                window.__mousePos = {
                    x: e.clientX,
                    y: e.clientY
                };
            }, true);
        })();
        """
        )

    def fix_boundary(self, parentIframes):
        html_selector = ' > '.join([
            *parentIframes,
            'html',
        ])

        print('HTML selector', html_selector, self._current_url, self.driver.current_url)

        if self.html_selector != html_selector or self._current_url != self.driver.current_url:
            with FrameContextDriver(self.driver, parentIframes):
                self._insert_mousemove_event_recorder()
                self.html = self.driver.find_element(By.CSS_SELECTOR, 'html')
                
                self.html_selector = html_selector
                self._current_url = self.driver.current_url

                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(self.html, 1, 0)
                actions.move_to_element_with_offset(self.html, -1, 0)
                actions.perform()

                self.saved_boundaries = self.driver.execute_script("""return window.__mousePos""")
                print('Setting up new boundary', self.saved_boundaries)


