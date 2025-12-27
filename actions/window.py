from .base import BaseAction

class ResizeAction(BaseAction):
    def execute(self):
        self.driver.set_window_size(self.params['width'], self.params['height'])

class LoadAction(BaseAction):
    def execute(self):
        url = self.params['location']
        if(self.driver.current_url == url):
            self.driver.refresh()
        else:
            self.driver.get(url)