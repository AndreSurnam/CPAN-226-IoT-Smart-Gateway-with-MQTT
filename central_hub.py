import paho.mqtt.client as mqtt
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)  # Web
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode="threading")  # Real-time web

# Initializing
devices = {}  # to store unique devices
isolated = set()  # to store isolated devices

""" 
    Using a public broker to establish publish-subsribe relationship and handle data 
    > used mqttprojects but this was old and not reliable anymore
    > used broker.hivemq.com but was slow

    > used mosquitto instead since it's much more compatible and faster
"""
mqttbroker = "test.mosquitto.org"

# Functions

# Triggers when the MQTT client successfully establishes with the broker


def on_connect(client, userdata, flags, rc, properties=None):
    if rc != 0:
        print(f"{rc}: Failed to connect to MQTT Broker")
        client.disconnect()
    else:
        print(f"{rc}: Connected to MQTT Broker")
        client.subscribe("TEMPERATURE/#")


""" 
    Triggers when the MQTT client recieves a msg from the broker on a subscribed topic
    > Topic: TEMPERATURE/Temperature_Sensor_1 (example) 
    > Message: 15 °C (example)
    > Decodes the byte into a string, then turns it into float
    Essentially the Smart Gateway component
    > Has automated device isolation in a form of IF statement

    SocketIO
    > emits an update everytime the callback is called to the script.js in real-time/dynamic updates
"""


def on_message(client, userdata, msg):
    temp = float(msg.payload.decode())
    device_id = msg.topic.split("/")[-1]

    status = "ACTIVE"

    """ 
        Checks if the device's status ISOLATED
        Does not update stored state
        Only reports status
    """
    if device_id in isolated:
        print(f"IGNORED: {device_id}")

    else:
        devices[device_id] = temp  # Applies temp (msg) to the device

        if temp > 30:  # Isolates the device and remains isolated
            isolated.add(device_id)
            status = "ISOLATED"

        # Dynamically send updates to dashboard (srcipt.js)
        socketio.emit("update", {
            "device": device_id,
            "temperature": temp,
            "status": status
        })

        print(f"EMITTING: {device_id} | {temp} °C | {status}")


# Creates a client that wraps a connection to the broker
client = mqtt.Client(
    client_id="Smart_Gateway", # Can be any name
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

# Connects
client.on_connect = on_connect
client.on_message = on_message

# Connects to the broker on port 1883 and a 60 seconds timer that reminds the broker it's still running
client.connect(mqttbroker, 1883, 60)
# Starts a background thread that continuosly proccesses network traffic
client.loop_start()

# Starts the home file


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# Starts app
if __name__ == "__main__":
    socketio.run(app, debug=True)
