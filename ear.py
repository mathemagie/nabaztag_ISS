"""ISS Tracker for Nabaztag Ear Control.

This module monitors the International Space Station's position and triggers
ear movements on a Nabaztag robot when the ISS flies over France. It polls
the Open Notify API every 10 seconds and sends commands via TCP socket.
"""

import socket
import logging
import requests
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_iss_location() -> dict:
    """Fetch the current ISS location from the Open Notify API.

    Returns:
        dict: ISS position containing 'latitude' and 'longitude' keys as strings.
              Returns empty dict on error.
    """
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        response.raise_for_status()
        iss_data = response.json()
        position = iss_data["iss_position"]
        logging.info(
            "ISS Current Location - Latitude: %s, Longitude: %s",
            position["latitude"],
            position["longitude"],
        )
        return position
    except requests.RequestException as e:
        logging.error("Request error: %s", e)
        return {}
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return {}


def is_iss_over_france(position: dict) -> bool:
    """Check if the ISS is currently over France.

    Uses a bounding box (41.0-51.0 lat, -5.0-9.0 lon) to determine if the ISS
    position falls within France's approximate geographic boundaries.

    Args:
        position: Dictionary containing 'latitude' and 'longitude' keys.

    Returns:
        bool: True if ISS is over France, False otherwise.
    """
    try:
        latitude = float(position.get("latitude", 0))
        longitude = float(position.get("longitude", 0))
        # France's approximate bounding box
        if 41.0 <= latitude <= 51.0 and -5.0 <= longitude <= 9.0:
            logging.info("ISS is currently over France.")
            return True
        else:
            logging.info("ISS is not over France.")
            return False
    except (ValueError, TypeError) as e:
        logging.error("Error processing position data: %s", e)
        return False


def simulate_nc(data: str, host: str, port: int) -> None:
    """Send data to a TCP server similar to netcat.

    Establishes a TCP connection, sends data, and receives a response.
    Used to communicate with the Nabaztag device over its control protocol.

    Args:
        data: String data to send (typically JSON commands).
        host: Target host address (e.g., 'localhost').
        port: Target port number (e.g., 1234).
    """
    try:
        logging.info("Connecting to %s:%d", host, port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            logging.info("Connection established")
            s.sendall(data.encode())
            logging.info("Sent data: %s", data)
            s.shutdown(socket.SHUT_WR)
            response = s.recv(1024)
            logging.info("Received response: %s", repr(response))
            print("Received", repr(response))
    except socket.error as e:
        logging.error("Socket error: %s", e)
        print(f"Socket error: {e}")
    except Exception as e:
        logging.error("An error occurred: %s", e)
        print(f"An error occurred: {e}")


def move_ears() -> None:
    """Send ear movement commands to the Nabaztag device.

    Sends a sequence of JSON-formatted ear position commands via TCP socket.
    Ear positions range from 0-17 per the pynab protocol.
    """
    data = (
        '{"type":"ears", "request_id":1, "left": 10, "right": 15}\n'
        '{"type":"ears", "request_id":2, "left": 5, "right": 0}\n'
    )
    logging.info("Starting send commands to nabaztag")
    # https://github.com/nabaztag2018/pynab/blob/master/PROTOCOL.md
    simulate_nc(data, "localhost", 1234)


if __name__ == "__main__":
    # Main loop: Monitor ISS position every 10 seconds and move ears when over France
    while 1:
        iss_position = get_iss_location()
        if is_iss_over_france(iss_position):
            move_ears()
            print("The ISS is currently over France.")
        else:
            print("The ISS is not over France.")
        time.sleep(10)
