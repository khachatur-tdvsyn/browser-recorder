
import json

from recorder.shortener import ClickActionsShortener, WheelActionsShortener, MouseMoveLinearShortener

LONG_OUTPUT = "events_output_mousemove.json"
SHORT_OUTPUT = "events_output_short.json"

with open(LONG_OUTPUT) as f:
    records = json.load(f)

records = ClickActionsShortener(records).shorten()
records = WheelActionsShortener(records).shorten()
records = MouseMoveLinearShortener(records).shorten()

with open(SHORT_OUTPUT, 'w') as f:
    json.dump(records, f)