import time
from browser import RecordableFirefoxBrowser

recordable = RecordableFirefoxBrowser("https://wikipedia.org", ["onclick"], record_input="events_output.json")
recordable.execute_record()
# recordable.start_recording()