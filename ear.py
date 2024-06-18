import socket
import logging
import requests
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_iss_location() -> dict:
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
    data = (
        '{"type":"ears", "request_id":1, "left": 10, "right": 15}\n'
        '{"type":"ears", "request_id":2, "left": 5, "right": 0}\n'
    )
    logging.info("Starting send commands to nabaztag")
    # https://github.com/nabaztag2018/pynab/blob/master/PROTOCOL.md
    simulate_nc(data, "localhost", 1234)


if __name__ == "__main__":
    while 1:
        iss_position = get_iss_location()
        if is_iss_over_france(iss_position):
            move_ears()
            print("The ISS is currently over France.")
        else:
            print("The ISS is not over France.")
        time.sleep(10)
