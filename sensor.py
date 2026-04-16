import paho.mqtt.client as mqtt
import threading
from random import uniform
import time

mqttbroker = "test.mosquitto.org"
threads = []  # Store threads to simulate multiple sensor devices


def temperature(device_id, min_temp, max_temp):
    client = mqtt.Client(
        client_id=device_id,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )  # Creates a client that wraps a connection to the broker

    client.connect(mqttbroker, 1883, 60)
    client.loop_start()

    """ 
        Continously generates temp and publishes the data 
        to the broker and gives said data to the subscribers
    """
    while True:
        temp = round(uniform(min_temp, max_temp), 2)
        topic = f"TEMPERATURE/{device_id}"

        client.publish(topic, temp)

        time.sleep(uniform(0.8, 1.15))


if __name__ == "__main__":
    # Create multiple simulated sensor devices
    devices = [
        ("Temperature_Sensor_1", 20, 40),  # default: min 20, max 40
        ("Temperature_Sensor_2", 20, 27),
        ("Temperature_Sensor_3", 20, 32),
        ("Temperature_Sensor_4", 30, 50),
        ("Temperature_Sensor_5", 15, 25),
        ("Temperature_Sensor_6", 25, 35)
    ]

    # Starts each simulated devices in its own thread
    for d in devices:
        th = threading.Thread(target=temperature, args=d)
        th.start()

        threads.append(th)
