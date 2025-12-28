
import json

from recorder.shortener import MouseActionsShortener

LONG_OUTPUT = "events_output.json"
SHORT_OUTPUT = "events_output_short.json"

with open(LONG_OUTPUT) as f:
    records = json.load(f)

print([*records[:4], '...'])
shortener = MouseActionsShortener(records)
records = shortener.shorten()

with open(SHORT_OUTPUT, 'w') as f:
    json.dump(records, f)