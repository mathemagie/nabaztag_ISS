import socket
import logging
import requests
import folium
import time
import datetime
from flask import Flask, render_template_string
import random


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


app = Flask(__name__)


@app.route("/iss-location-json")
def get_iss_location_json():
    # fake_data = {
    #     "latitude": str(random.uniform(-90, 90)),
    #     "longitude": str(random.uniform(-180, 180)),
    #     "timestamp": int(time.time()),
    # }
    # return fake_data
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        position = data["iss_position"]
        latitude = float(position["latitude"])
        longitude = float(position["longitude"])
        logging.info(
            "ISS Current Location - Latitude: %s, Longitude: %s", latitude, longitude
        )
        if 41.0 <= latitude <= 51.0 and -5.0 <= longitude <= 9.0:
            logging.info("The ISS is currently over France.")
            print("The ISS is currently over France.")
            send_commands()
        else:
            logging.info("The ISS is not over France.")
            print("The ISS is not over France.")
        return {
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    else:
        logging.error("Failed to retrieve ISS location")
        return {"error": "Failed to retrieve ISS location"}, response.status_code


@app.route("/")
def new_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        position = data["iss_position"]
        latitude = float(position["latitude"])
        longitude = float(position["longitude"])
        logging.info(
            "ISS Current Location - Latitude: %s, Longitude: %s", latitude, longitude
        )
        print(f"ISS Current Location - Latitude: {latitude}, Longitude: {longitude}")

        # Create a map centered at the ISS location
        iss_map = folium.Map(
            location=[latitude, longitude], zoom_start=5, tiles="openstreetmap"
        )
        folium.Marker([latitude, longitude], tooltip="ISS Current Location").add_to(
            iss_map
        )
        # Render the map to an HTML string
        iss_map._repr_html_()

        try:
            return render_template_string(
                """
                <html>
                    <head>
                        <title>ISS Current Location</title>
                        <meta http-equiv="refresh" content="50">
                        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
                        <script>
                            $(document).ready(function() {
                                var marker;
                                var map = new L.Map('map').setView([{{ latitude }}, {{ longitude }}], 5);
                                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                }).addTo(map);
                                marker = new L.Marker([{{ latitude }}, {{ longitude }}]).addTo(map)
                                    .bindPopup('ISS Current Location<br>Latitude: {{ latitude }}<br>Longitude: {{ longitude }}<br>Timestamp: {{ current_time }}')
                                    .openPopup();
                                setInterval(function() {
                                    $.ajax({
                                        url: "/iss-location-json",
                                        success: function(data) {
                                            $('#latitude').text(data.latitude);
                                            $('#longitude').text(data.longitude);
                                            $('#timestamp').text(data.timestamp);
                                            var newLatLng = new L.LatLng(data.latitude, data.longitude);
                                            marker.setLatLng(newLatLng);
                                            map.setView(newLatLng, map.getZoom());
                                            marker.bindPopup('ISS Current Location<br>Latitude: ' + data.latitude + '<br>Longitude: ' + data.longitude + '<br>Timestamp: ' + data.timestamp).openPopup();
                                        },
                                        error: function() {
                                            console.error("Failed to retrieve ISS location");
                                        }
                                    });
                                }, 20000); // 30 seconds
                            });
                        </script>
                    </head>
                    <body>
                        <div id="map" style="position:absolute; top:0; bottom:0; right:0; left:0;">
                            <div style="position:absolute; top:10px; left:10px; background-color:white; padding:10px; border-radius:5px;">
                                <h1>ISS Current Location</h1>
                                <div>Latitude: <span id="latitude">{{ latitude }}</span></div>
                                <div>Longitude: <span id="longitude">{{ longitude }}</span></div>
                                <div>Timestamp: <span id="timestamp">{{ current_time }}</span></div>
                            </div>
                        </div>
                    </body>
                </html>
                """,
                latitude=latitude,
                longitude=longitude,
                current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        except Exception as e:
            logging.error("Error rendering template: %s", e)
            print(f"Error rendering template: {e}")
            return "An error occurred while rendering the template", 500
    else:
        logging.error("Failed to retrieve ISS location")
        return "Failed to retrieve ISS location", response.status_code


# @app.route('/old')
# def get_iss_location():
#     url = "http://api.open-notify.org/iss-now.json"
#     response = requests.get(url, timeout=10)
#     if response.status_code == 200:
#         data = response.json()
#         position = data["iss_position"]
#         latitude = float(position["latitude"])
#         longitude = float(position["longitude"])
#         logging.info(
#             "ISS Current Location - Latitude: %s, Longitude: %s", latitude, longitude
#         )
#         print(f"ISS Current Location - Latitude: {latitude}, Longitude: {longitude}")

#         # Create a map centered at the ISS location
#         iss_map = folium.Map(location=[latitude, longitude], zoom_start=5, tiles='openstreetmap')
#         folium.Marker([latitude, longitude], tooltip="ISS Current Location").add_to(
#             iss_map
#         )
#         # Render the map to an HTML string
#         map_html = iss_map._repr_html_()

#         # Check if ISS is over France
#         if 41.0 <= latitude <= 51.0 and -5.0 <= longitude <= 9.0:
#             logging.info("The ISS is currently over France.")
#             print("The ISS is currently over France.")
#             send_commands()
#         else:
#             logging.info("The ISS is not over France.")
#             print("The ISS is not over France.")

#         try:
#             return render_template_string("""
#                 <html>
#                     <head>
#                         <title>ISS Current Location</title>
#                         <meta http-equiv="refresh" content="60">
#                     </head>
#                     <body>
#                         <h1>ISS Current Location - Current Time: {{ current_time }}</h1>
#                         <div>{{ map_html|safe }}</div>
#                     </body>
#                 </html>
#                 """, map_html=map_html, current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         except Exception as e:
#             logging.error(f"Error rendering template: {e}")
#             print(f"Error rendering template: {e}")
#             return "An error occurred while rendering the template", 500
#     else:
#         logging.error("Failed to retrieve ISS location")
#         print("Failed to retrieve ISS location")
#         return "Failed to retrieve ISS location", 500

if __name__ == "__main__":
    app.run(debug=True)
