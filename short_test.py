
import json

from recorder.shortener import MouseActionsShortener, WheelActionsShortener

LONG_OUTPUT = "events_output.json"
SHORT_OUTPUT = "events_output_short.json"

with open(LONG_OUTPUT) as f:
    records = json.load(f)

records = MouseActionsShortener(records).shorten()
records = WheelActionsShortener(records).shorten()

with open(SHORT_OUTPUT, 'w') as f:
    json.dump(records, f)