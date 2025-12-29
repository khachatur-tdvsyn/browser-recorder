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

### Running the Application

```bash
python main.py --url "https://example.com"
```

### Command Line Arguments

- `--url, -u`: Target URL to open in the browser
- `--input-file, -i`: Path to input file (default: events_output.json)
- `--output-file, -o`: Path to output file (default: events_output.json)
- `--execute, -e`: Execute recorded interactions on startup
- `--record, -r`: Start recording immediately on startup
- `--verbose, -V`: Enable verbose logging output
- `--allowed-events`: List of allowed event names to record

### Interactive Commands

Once the application is running, you can use the following commands in the interactive console:

| Command | Aliases | Description | Usage |
|---------|---------|-------------|-------|
| **record** | `r` | Start recording user interactions in browser | `record [output_file]` |
| **play** | `pl` | Resume playing recorded interactions | `play` |
| **pause** | `p` | Pause recording or playback | `pause` |
| **stop** | `s` | Stop recording user interactions | `stop` |
| **execute** | `e` | Execute recorded interactions from a file | `execute [input_file]` |
| **help** | `h`, `?` | Show all available commands and their usage | `help` |
| **exit** | `quit`, `close` | Close the program | `exit` |

### Example Workflow

```bash
# Start the application
python main.py --url "https://example.com"

# In the interactive console:
Browser recorder > record output.json
# ... Interact with the browser ...
Browser recorder > stop

# Execute the recorded interactions
Browser recorder > execute output.json

# Get help on available commands
Browser recorder > help

# Exit the application
Browser recorder > exit
```

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

## Adding New Commands

To add new commands to the interactive interface:

1. Create a new command class in `browser/command.py` inheriting from `Command`
2. Define `names` (tuple of command aliases), `description`, and `usage` attributes
3. Implement the `execute()` method
4. Register the command in `main.py` by adding it to the CommandProcessor's command list

### Example Command

```python
class MyCommand(Command):
    names = ("mycommand", "mc")
    description = "Description of what this command does"
    usage = "mycommand [argument]"

    def execute(self, argument=None):
        # Your implementation here
        pass
```

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

## Future Enhancements

- Support for additional browsers (Chrome, Edge, Safari)
- Event deduplication and optimization
- CLI for recording and playback management
## License

This project is provided as-is for educational and automation purposes.
