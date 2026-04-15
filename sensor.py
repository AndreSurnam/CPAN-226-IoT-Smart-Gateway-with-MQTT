import paho.mqtt.client as mqtt
import threading
from random import uniform
import time

mqttbroker = "broker.hivemq.com"
threads = []


def temperature(device_id, min_temp, max_temp,):
    client = mqtt.Client(
        client_id=device_id,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    client.connect(mqttbroker, 1883, 60)
    client.loop_start()

    while True:
        temp = round(uniform(min_temp, max_temp), 2)
        topic = f"TEMPERATURE/{device_id}"

        client.publish(topic, temp)
        print(f"{device_id}: {temp}")

        time.sleep(3)


if __name__ == "__main__":
    devices = [
        ("sensor_1", 20, 40),  # default: min 20, max 40
        ("sensor_2", 25, 35),
        ("sensor_3", 20, 32),
        ("sensor_4", 30, 50),
        ("sensor_5", 15, 25)
    ]

    try:
        for d in devices:
            th = threading.Thread(target=temperature, args=d)
            th.start()

            threads.append(th)

    except KeyboardInterrupt:
        print("Force Stop")
