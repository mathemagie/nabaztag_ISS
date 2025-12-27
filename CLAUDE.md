# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based IoT project that makes a Nabaztag/tag:tag robot's ears move whenever the International Space Station (ISS) flies over France (or any configurable geographic region). The project combines real-time ISS tracking with vintage smart toy control.

## Architecture

### Core Components

- **`ear.py`**: Main monitoring script with three key functions:
  - `get_iss_location()`: Polls the Open Notify API (http://api.open-notify.org/iss-now.json) every 10 seconds to retrieve current ISS coordinates
  - `is_iss_over_france(position)`: Checks if ISS coordinates fall within configurable geographic boundaries (default: France bounding box 41.0-51.0 lat, -5.0-9.0 lon)
  - `move_ears()`: Sends ear movement commands via TCP socket to Nabaztag device
  - Main loop: Continuously monitors ISS position and triggers ear movements when ISS enters configured region

### Communication Protocol

- **Nabaztag Protocol**: Uses the pynab protocol (https://github.com/nabaztag2018/pynab/blob/master/PROTOCOL.md)
- **Connection**: TCP socket connection to `localhost:1234` (configurable)
- **Command Format**: JSON-based ear commands sent over TCP:
  ```json
  {"type":"ears", "request_id":1, "left": 10, "right": 15}
  {"type":"ears", "request_id":2, "left": 5, "right": 0}
  ```
- **Network Setup**: Expects SSH tunnel or direct local network access to Nabaztag device

### Deleted Files (from git history)

- `mescommandes.json`: Previously stored ear command definitions (now hardcoded in `ear.py:70-73`)
- `send.py`: Network communication helper (functionality now integrated into `ear.py:49-66` via `simulate_nc()`)

## Running the Project

### Basic Execution
```bash
python ear.py
```

### Dependencies
The project uses standard Python libraries:
- `requests`: For ISS API calls
- `socket`: For Nabaztag TCP communication
- `logging`: For structured logging output
- `time`: For polling intervals

Note: No `requirements.txt` exists yet. If creating one:
```
requests>=2.25.0
```

### Network Setup

The script expects a Nabaztag to be accessible at `localhost:1234`. To establish this connection:

**SSH Tunnel Method** (if Nabaztag is on remote network):
```bash
ssh -L 1234:nabaztag-local-ip:1234 user@gateway
```

**Direct Connection** (if on same network): Update `ear.py:76` with Nabaztag's actual IP address

## Configuration

### Geographic Region
Modify the bounding box coordinates in `ear.py:38` in the `is_iss_over_france()` function:
```python
if 41.0 <= latitude <= 51.0 and -5.0 <= longitude <= 9.0:
```

### Polling Frequency
Adjust the sleep interval in `ear.py:87`:
```python
time.sleep(10)  # seconds between ISS position checks
```

### Ear Movement Commands
Modify the JSON commands in `ear.py:70-73`:
```python
data = (
    '{"type":"ears", "request_id":1, "left": 10, "right": 15}\n'
    '{"type":"ears", "request_id":2, "left": 5, "right": 0}\n'
)
```
Values for `left` and `right` control ear positions (0-17 range based on pynab protocol)

### Network Connection
Change host/port in `ear.py:76`:
```python
simulate_nc(data, "localhost", 1234)
```

## Development Notes

- The project has no test suite currently
- Logging is configured at INFO level; outputs ISS coordinates and connection status to console
- Error handling is implemented for API requests and socket connections
- The main loop runs indefinitely; use Ctrl+C to stop
- No linting or build configuration exists

## External Dependencies

- **ISS Tracking API**: http://api.open-notify.org/iss-now.json (free, no API key required)
- **Nabaztag Hardware**: Requires physical Nabaztag/tag:tag device on network
- **Web Tracker**: Live demo available at https://mathemagie.github.io/hack/nabaztag_iss/

## API Response Format

The Open Notify API returns:
```json
{
  "iss_position": {
    "latitude": "12.3456",
    "longitude": "78.9012"
  },
  "message": "success",
  "timestamp": 1234567890
}
```
