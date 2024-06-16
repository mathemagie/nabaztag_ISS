# Establish an SSH tunnel to the remote server
ssh -L 1234:127.0.0.1:10543 pi@192.168.1.17

# Send the contents of mescommandes.json to the local port 1234 using netcat
cat mescommandes.json | nc -4 -w 5 -v localhost 1234

# Overview
This script establishes a network connection to a specified host and port, sends predefined JSON data, and logs the entire communication process. It is designed to replicate the functionality of the `nc` (netcat) command.

# Requirements
- Python 3.x
- Internet connection (if connecting to a remote host)

# Installation
1. Clone the repository or download the script.
2. Ensure Python 3 is installed on your system.

# Usage
1. Open a terminal.
2. Navigate to the directory containing the `send.py` script.
3. Execute the script with the following command:
   ```sh
   python send.py
   ```
