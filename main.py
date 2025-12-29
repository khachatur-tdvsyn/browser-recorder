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

from argparse import ArgumentParser

records = ["onclick", "ondblclick", "onmousedown", "onmouseup", "onkeydown", "onkeyup", "onwheel", "oncut", "oncopy", "onpaste", "onresize", "onload", "onbeforeunload"]

def parse_arguments():
    parser = ArgumentParser("Browser Recorder", description="A Python-based tool for recording and replaying browser interactions using Selenium. This project captures user events (clicks, keyboard input, mouse movements, etc.) from web browsers and can replay them automatically.")
    parser.add_argument(
        "--url", "-u",
        type=str,
        help="Target URL"
    )

    parser.add_argument(
        "--input-file", "-i",
        type=str,
        help="Path to input file",
        default="events_output.json"
    )

    parser.add_argument(
        "--output-file", "-o",
        type=str,
        help="Path to output file",
        default="events_output.json"
    )

    parser.add_argument(
        "--execute", "-e",
        action="store_true",
        help="Execute the main action"
    )

    parser.add_argument(
        "--record", "-r",
        action="store_true",
        help="Record execution details"
    )

    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--allowed-events",
        type=str,
        nargs="*",
        default=records,
        help="List of allowed event names"
    )

    parser.add_argument(
        "--timeout", "-t",
        type=float,
        default=30,
        help="Timeout in seconds (default: 30)"
    )

    return parser.parse_args()

record = False
#url = "https://wikipedia.org"
url = "https://hy.wikipedia.org/wiki/%D5%80%D5%A1%D5%B5%D5%A1%D5%BD%D5%BF%D5%A1%D5%B6"
# url = "https://www.w3schools.com/js/tryit.asp?filename=tryjs_whereto_url_relative"
# url = "https://google.com"

arguments = parse_arguments()



recordable = RecordableFirefoxBrowser(
    start_url=arguments.url, 
    recordable_events=arguments.allowed_events, 
    record_output=arguments.input_file, 
    record_input=arguments.input_file,
    records_storage=JSONEventStorage()
)

processor = CommandProcessor([
    RecordCommand(recordable),
    PlayCommand(recordable),
    PauseCommand(recordable),
    StopCommand(recordable),
    ExecuteCommand(recordable),
])

if arguments.execute:
    recordable.execute_record()
elif arguments.record:
    recordable.start_recording()

while True:
    text = input("Browser recorder > ")
    if text in ("exit", "quit"):
        break
    processor.process(text)