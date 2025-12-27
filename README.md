# 🐰🌌 Lapin cosmique

> *A whimsical IoT project: My Nabaztag robot's ears wiggle every time the International Space Station flies over France. Live tracking + open source code.*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20Tracker-blue)](https://mathemagie.github.io/bidouille/lapin_cosmique/)
[![Python](https://img.shields.io/badge/Python-3.x-green)](https://www.python.org/)

## ✨ What Is This?

Imagine a vintage smart rabbit from 2005 that gets excited every time the International Space Station passes overhead. That's exactly what this project does!

My **Nabaztag** robot (a delightful IoT toy from the mid-2000s) wiggles its ears in real-time whenever the ISS enters French airspace. It's a playful bridge between Earth and space—turning orbital mechanics into delightful rabbit ear choreography.

**🎥 [Watch the Demo Video](https://mathemagie.github.io/bidouille/lapin_cosmique/)** | **🌐 [Live ISS Tracker](https://mathemagie.github.io/bidouille/lapin_cosmique/)**

## 🎯 Project Overview

This project combines:
- **Real-time ISS tracking** via the [Open Notify API](http://api.open-notify.org/iss-now.json)
- **Vintage IoT hardware** ([Nabaztag/tag:tag](https://www.multiplie.fr/nabaztag/) rabbit from 2005-2011)
- **Python automation** that monitors space and controls physical movement
- **A beautiful web interface** for live tracking

When the ISS enters French airspace (or any region you configure), the Python script sends HTTP commands to your Nabaztag, making its iconic ears spring to life. It's simple magic: space tracking meets vintage smart toys.

## 🚀 Quick Start

### Prerequisites

- **Nabaztag or tag:tag rabbit** (vintage smart toy, 2005-2011)
- **Raspberry Pi** or similar device to run the Python script
- **Python 3.x** installed
- **Local network connection** to your Nabaztag device
- **SSH access** to your Nabaztag (if using SSH tunnel method)

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/mathemagie/lapin_cosmique.git
   cd lapin_cosmique
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Nabaztag connection**
   
   By default, the script connects to `localhost:1234`. To change this, edit the `simulate_nc()` call in `ear.py`:
   ```python
   # Line 76 in ear.py
   simulate_nc(data, "localhost", 1234)  # Change host and port as needed
   ```
   
   If your Nabaztag is on a remote network, set up an SSH tunnel first (see SSH Tunnel Setup section below).

4. **Customize your region** (optional)
   
   By default, the script monitors French airspace. To change this, edit the coordinates in the `is_iss_over_france()` function in `ear.py`:
   ```python
   # Line 38 in ear.py
   if 41.0 <= latitude <= 51.0 and -5.0 <= longitude <= 9.0:  # France boundaries
   # Change to your desired region's coordinates
   ```

5. **Run the script**
   ```bash
   python ear.py
   ```

The script will continuously monitor the ISS position and trigger your Nabaztag's ears whenever the station enters your configured region!

## 📖 How It Works

### The Magic Behind the Ears

1. **ISS Monitoring**: The Python script (`ear.py`) polls the [Open Notify API](http://api.open-notify.org/iss-now.json) every 10 seconds to get the current ISS position.

2. **Region Detection**: It checks if the ISS coordinates fall within your configured geographic boundaries (default: France).

3. **Ear Activation**: When the ISS enters the region, the script sends TCP socket commands to your Nabaztag device, triggering ear movement commands.

4. **Continuous Tracking**: The script runs in a loop, keeping the Nabaztag synchronized with the ISS's orbit.

### Technical Details

- **API Communication**: Uses Python's `requests` library to fetch ISS data
- **Network Protocol**: TCP socket connection to Nabaztag (default: `localhost:1234`)
- **Command Format**: JSON commands hardcoded in `ear.py` (lines 70-73) using pynab protocol
- **SSH Tunnel**: Optional SSH tunnel support for remote Nabaztag access

## 📁 Project Files

| File | Description |
|------|-------------|
| `ear.py` | Main monitoring script that tracks ISS and controls Nabaztag |
| `requirements.txt` | Python package dependencies |

## 🛠️ Hardware Setup

### Nabaztag Requirements

- **Nabaztag** or **tag:tag** rabbit (original models from 2005-2011)
- Device must be accessible via TCP socket connection (default port 1234)
- Nabaztag should be on the same local network, or accessible via SSH tunnel

### Finding Your Nabaztag's IP Address

1. Check your router's connected devices list
2. Look for a device named "Nabaztag" or "tag:tag"
3. Alternatively, use network scanning tools:
   ```bash
   nmap -sn 192.168.1.0/24  # Replace with your network range
   ```

### SSH Tunnel Setup (Optional)

If your Nabaztag is on a different network or requires SSH access:

```bash
ssh -L 1234:nabaztag-ip:1234 user@gateway
```

The script will connect to `localhost:1234`, which will be forwarded to your Nabaztag via the SSH tunnel.

## ⚙️ Configuration

### Customizing Geographic Regions

Edit the boundary coordinates in the `is_iss_over_france()` function in `ear.py` (line 38):

```python
# Example: United States (continental)
if 24.5 <= latitude <= 49.4 and -125.0 <= longitude <= -66.9:

# Example: United Kingdom
if 50.0 <= latitude <= 60.0 and -8.0 <= longitude <= 2.0:

# Example: Japan
if 24.0 <= latitude <= 46.0 and 123.0 <= longitude <= 146.0:
```

### Adjusting Update Frequency

Change the polling interval in `ear.py` (line 87):

```python
time.sleep(10)  # Check every 10 seconds (default)
# Change to:
time.sleep(5)  # Check every 5 seconds
```

### Customizing Ear Movements

Edit the ear movement commands in the `move_ears()` function in `ear.py` (lines 70-73):

```python
data = (
    '{"type":"ears", "request_id":1, "left": 10, "right": 15}\n'
    '{"type":"ears", "request_id":2, "left": 5, "right": 0}\n'
)
```

The `left` and `right` values control ear positions (0-17 range based on pynab protocol). Adjust these values to create different ear movement patterns.

## 🎨 Usage Examples

### Basic Usage

```bash
# Run the monitoring script
python ear.py
```

### Running as a Service (Linux)

Create a systemd service file `/etc/systemd/system/nabaztag-iss.service`:

```ini
[Unit]
Description=Lapin cosmique
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/lapin_cosmique
ExecStart=/usr/bin/python3 /home/pi/lapin_cosmique/ear.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable nabaztag-iss.service
sudo systemctl start nabaztag-iss.service
```

### Running in Background

```bash
# Using nohup
nohup python ear.py > nabaztag.log 2>&1 &

# Using screen
screen -S nabaztag
python ear.py
# Press Ctrl+A then D to detach
```

## 🌍 Customizing for Different Countries

The script is easily adaptable to any geographic region. Here are some example coordinates:

| Country/Region | Min Lat | Max Lat | Min Lon | Max Lon |
|----------------|---------|---------|---------|---------|
| France | 41.3 | 51.1 | -5.1 | 8.2 |
| United States (Continental) | 24.5 | 49.4 | -125.0 | -66.9 |
| United Kingdom | 50.0 | 60.0 | -8.0 | 2.0 |
| Germany | 47.3 | 55.1 | 5.9 | 15.0 |
| Japan | 24.0 | 46.0 | 123.0 | 146.0 |
| Australia | -44.0 | -10.0 | 113.0 | 154.0 |
| Brazil | -33.7 | 5.3 | -73.9 | -32.4 |

Simply update the coordinates in `ear.py` to match your desired region!

## 🔗 Related Resources

- **🌐 [Live Web Tracker](https://mathemagie.github.io/bidouille/lapin_cosmique/)** - Real-time ISS tracking with interactive map
- **📡 [Open Notify API](http://api.open-notify.org/)** - Free ISS tracking API
- **🐰 [Nabaztag Information](https://www.multiplie.fr/nabaztag/)** - Learn about the Nabaztag and TagTagTag revival kit
- **📚 [Nabaztag API Documentation](http://www.nabaztag.com/vl/FR/api.jsp)** - Official Nabaztag API reference

## 🤝 Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation, your help makes this project better.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions

- Support for additional Nabaztag models
- Custom ear movement patterns
- Integration with other space APIs
- Web dashboard improvements
- Documentation enhancements
- Support for multiple Nabaztags

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Open Notify** - For providing the free ISS tracking API
- **Nabaztag Community** - For keeping these delightful robots alive
- **Open Source Community** - For inspiration and support

## 📸 Screenshots

![ISS Tracker Map](https://mathemagie.github.io/bidouille/lapin_cosmique/screenshot-map.png)

*Live ISS tracking map showing current position*

---

**Made with 🌌 for space enthusiasts and IoT hobbyists**

*Turning orbital mechanics into rabbit ear choreography since 2024*

