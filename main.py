from browser.browser import RecordableFirefoxBrowser
from storage.json import JSONEventStorage
from browser.command import (
    CommandProcessor,
    RecordCommand,
    PlayCommand,
    PauseCommand,
    StopCommand,
    ExecuteCommand
)

record = False
#url = "https://wikipedia.org"
url = "https://hy.wikipedia.org/wiki/%D5%80%D5%A1%D5%B5%D5%A1%D5%BD%D5%BF%D5%A1%D5%B6"
# url = "https://www.w3schools.com/js/tryit.asp?filename=tryjs_whereto_url_relative"
# url = "https://google.com"

records = ["onclick", "ondblclick", "onmousedown", "onmouseup", "onkeydown", "onkeyup", "onwheel", "oncut", "oncopy", "onpaste", "onresize", "onload", "onbeforeunload"]

default_record_output = "events_output.json"
default_record_intput = "events_output.json"

recordable = RecordableFirefoxBrowser(
    start_url=url, 
    recordable_events=records, 
    record_output=default_record_output, 
    record_input=default_record_intput,
    records_storage=JSONEventStorage()
)

processor = CommandProcessor([
    RecordCommand(recordable),
    PlayCommand(recordable),
    PauseCommand(recordable),
    StopCommand(recordable),
    ExecuteCommand(recordable),
])

while True:
    text = input("Browser recorder > ")
    if text in ("exit", "quit"):
        break
    processor.process(text)