from browser.browser import RecordableFirefoxBrowser

record = False
# url = "https://wikipedia.org"
# url = "https://www.w3schools.com/js/tryit.asp?filename=tryjs_whereto_url_relative"
url = "https://google.com"

records = ["onclick", "ondblclick", "onmousedown", "onmouseup", "onkeydown", "onkeyup", "onwheel", "oncut", "oncopy", "onpaste", "onresize", "onload", "onbeforeunload"]

recordable = RecordableFirefoxBrowser(url, records, record_output="events_output.json", record_input="events_output.json")
recordable.start()