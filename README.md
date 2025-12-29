# Browser Recorder

A Python-based tool for recording and replaying browser interactions using Selenium. This project captures user events (clicks, keyboard input, mouse movements, etc.) from web browsers and can replay them automatically.

## Features

- **Event Recording**: Captures a wide range of browser events including:
  - Mouse events: click, double-click, mousedown, mouseup, mousemove, wheel
  - Keyboard events: keydown, keyup
  - Clipboard events: cut, copy, paste
  - Window events: resize, load, beforeunload

- **Multi-frame Support**: Records and replays events from both main page and iframe elements
- **Boundary Calculation**: Automatically calculates element positions relative to the viewport, accounting for iframe offsets
- **Event Storage**: Saves recorded events to JSON files for later replay or analysis
- **Action Replay**: Executes recorded events with precise positioning and timing
- **Firefox Browser**: Full support for Firefox WebDriver automation

## Project Structure

```
browser_recorder/
├── actions/              # Action execution classes
│   ├── base.py          # Base action classes
│   ├── mouse.py         # Mouse event actions (click, drag, etc.)
│   ├── keyboard.py      # Keyboard event actions
│   ├── clipboard.py     # Clipboard event actions
│   ├── window.py        # Window event actions
│   └── factory.py       # Factory pattern for action creation
├── browser/             # Browser automation and recording
│   ├── browser.py       # Main browser recorder class
│   └── context.py       # Frame context management
├── recorder/            # Event recording logic
│   ├── recorder.py      # Event capturing and boundary calculation
│   └── shortener.py     # Event normalization and optimization
├── js_utils.py          # JavaScript payloads for event injection
├── main.py              # Example usage script
└── README.md            # This file
```

## Requirements

- Python 3.8 or higher
- Selenium WebDriver 4.0+
- Firefox browser
- geckodriver (Firefox WebDriver executable)

### Installation

```bash
# Install required Python packages
pip install selenium

# Download geckodriver from https://github.com/mozilla/geckodriver/releases
# Add geckodriver to your system PATH or specify the path in the code
```

## Usage

### Basic Example

```python
from browser.browser import RecordableFirefoxBrowser

# Initialize the recorder
url = "https://google.com"
events = ["onclick", "ondblclick", "onmousedown", "onmouseup", "onkeydown", "onkeyup", "onwheel", "oncut", "oncopy", "onpaste", "onresize", "onload", "onbeforeunload"]

recorder = RecordableFirefoxBrowser(
    url=url,
    records=events,
    record_output="events_output.json",
    record_input="events_output.json"
)

# Start recording (browser window will open)
recorder.start()
```

### Playback Mode

When `record=False`, the recorder will:
1. Open the browser
2. Load recorded events from the input file
3. Replay all recorded actions automatically
4. Close the browser

## Limitations

### Known Issues

- **Drag and Drop**: Full drag-and-drop replication is limited. Current implementation uses clipboard and keyboard shortcuts as workarounds for select events
- **Cross-Origin iframes**: Cannot capture events from iframes with different origins due to browser security restrictions (Same-Origin Policy)
- **Select Events**: Select event handling is limited to input and textarea elements
- **Scroll Events**: Scroll events are implicitly captured through mousedown and mouseup events, but explicit scroll actions may not be fully replayed

### Scope Limitations

- **Single Browser**: Currently supports Firefox only
- **Event Normalization**: Some redundant events (e.g., onclick when onmousedown/onmouseup are present) are not automatically removed
- **Complex Interactions**: Some modern web interactions (animations, asynchronous loading, etc.) may not replay correctly
- **Session State**: Recorded interactions are tied to specific page structure and may fail if DOM elements change

## Configuration

### Event Types

Specify which events to record by passing a list to the `records` parameter:

```python
events_to_capture = [
    "onclick",           # Click events
    "ondblclick",        # Double-click events
    "onmousedown",       # Mouse button down
    "onmouseup",         # Mouse button up
    "onmousemove",       # Mouse movement
    "onwheel",           # Mouse wheel scroll
    "onkeydown",         # Key press down
    "onkeyup",           # Key press up
    "oncut",             # Cut action
    "oncopy",            # Copy action
    "onpaste",           # Paste action
    "onresize",          # Window resize
    "onload",            # Page load
    "onbeforeunload"     # Before page unload
]
```

### File Paths

- `record_output`: Path to save recorded events (JSON format)
- `record_input`: Path to load recorded events for playback

## Development Notes

### Event Storage Format

Events are stored in JSON format with the following structure:

```json
[
  {
    "action": "onclick",
    "element": "CSS selector of the target element",
    "x": 100,
    "y": 200,
    "timestamp": 1234567890,
    ...
  },
  ...
]
```

### Extending the Project

To add new event types:

1. Create a new action class in `actions/` directory inheriting from `BaseAction` or `MouseBaseAction`
2. Register it in `ActionFactory.avaiable_actions`
3. Add event capturing logic in `js_utils.py` if needed

## Future Enhancements

- Support for additional browsers (Chrome, Edge, Safari)
- Event deduplication and optimization
- CLI for recording and playback management
## License

This project is provided as-is for educational and automation purposes.
