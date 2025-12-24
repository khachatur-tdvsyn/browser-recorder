from browser import RecordableFirefoxBrowser

record = False
url = "https://google.com"

if record:
    recordable = RecordableFirefoxBrowser(url, ["onclick", "onmousedown", "onmouseup"], record_output="events_output.json")
    recordable.start_recording()
else:
    replayable = RecordableFirefoxBrowser(url, record_input="events_output.json")
    replayable.execute_record()