import time
import json

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchWindowException, InvalidSessionIdException

from js_utils import  (
    EVENT_LIST_PAYLOAD, 
    EVENT_LISTENER_INJECTED_PAYLOAD,
    GET_CSS_SELECTOR_PAYLOAD,
    get_event_recorder_payload,
)
from actions import ActionFactory
from recorder import BoundaryRecorder


class RecordableBrowser(ABC):
    type: str
    executable_path: Optional[Path | str] = None
    is_recording: bool = False
    record_output: Optional[Path | str] = None
    record_input: Optional[Path | str] = None
    recordable_events: Optional[list[str]] = None

    @abstractmethod
    def init_browser(self): ...

    @abstractmethod
    def start_recording(self):
        self.is_recording = True

    @abstractmethod
    def stop_recording(self): 
        self.is_recording = False

    @abstractmethod
    def execute_record(self): ...


class RecordableFirefoxBrowser(RecordableBrowser):
    def __init__(
        self,
        start_url: Optional[str]=None,
        recordable_events: Optional[list[str]] = None,
        record_input=None,
        record_output=None,
        executable_path=None,
        options: Options | None = None,
    ):
        self.record_input = record_input
        self.start_url = start_url
        self.record_output = record_output
        self.executable_path = executable_path
        self.browser = None
        self.browser_options = options
        self.recordable_events = recordable_events

        self.js_payload = get_event_recorder_payload(self.recordable_events)
        self.init_browser()

        self.record_buffer = []

    def init_browser(self):
        print('Opening browser, please wait...')
        self.browser = webdriver.Firefox(options=self.browser_options)
        print('Browser opened')
        if(self.start_url):
            self.browser.get(self.start_url)
        
        self.boundary_recorder = BoundaryRecorder(self.browser)


    def save_output(self):
        if self.record_output:
            with open(self.record_output, "w+") as f:
                print(self.record_buffer)
                json.dump(self.record_buffer, f)
        else:
            print(self.record_buffer)

    def start_recording(self):
        super().start_recording()
        self.browser.execute_script(self.js_payload)
        print('Executing initial JS')

        self.title = self.browser.title
        while self.is_recording:
            try:
                if self.title != self.browser.title:
                    print('Re-execute script')
                    self.browser.execute_script(self.js_payload)
                    self.title = self.browser.title
                elif not self.browser.execute_script(EVENT_LISTENER_INJECTED_PAYLOAD):
                    print('Re-inject event listeners')
                    self.browser.execute_script(self.js_payload)
            
                events = self.browser.execute_script(EVENT_LIST_PAYLOAD)
                self.record_buffer += events or []

                for e in events:
                    print(e.get('time'), ':', e.get('type'))

                time.sleep(0.125)
            except NoSuchWindowException:
                print("Window closed. Stop recording")
                break
            except InvalidSessionIdException as e:
                print('Something is wrong with WebDriver session :|', e)
                break
        
        self.save_output()
    
    def stop_recording(self):
        super().stop_recording()
    
    def execute_record(self):
        with open(self.record_input) as f:
            execution_record = json.load(f)
        
        actions = ActionFactory.create_action(self.browser, execution_record, self.boundary_recorder)
        
        start = time.time()
        print('Starting execution of recorded events...')
        for a in actions:
            a.execute()
        
        end = time.time()
        print(f'Execution finished in {end - start:.3f} seconds.')
