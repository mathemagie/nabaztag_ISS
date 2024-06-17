import socket
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def simulate_nc(data, host, port):
    logging.info(f"Connecting to {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        logging.info("Connection established")
        s.sendall(data.encode())
        logging.info(f"Sent data: {data}")
        s.shutdown(socket.SHUT_WR)
        response = s.recv(1024)
        logging.info(f"Received response: {repr(response)}")
        print("Received", repr(response))


def send_commands():
    data = (
        '{"type":"ears", "request_id":1, "left": 10, "right": 15}\n'
        '{"type":"ears", "request_id":2, "left": 5, "right": 0}\n'
    )
    logging.info("Starting send commands to nabaztag")
    # https://github.com/nabaztag2018/pynab/blob/master/PROTOCOL.md
    simulate_nc(data, "localhost", 1234)


if __name__ == "__main__":
    send_commands()