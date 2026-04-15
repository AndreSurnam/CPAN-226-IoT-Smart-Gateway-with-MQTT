import paho.mqtt.client as mqtt

devices = {}
isolated = set()

mqttbroker = "broker.hivemq.com"

def on_message(client, userdata, msg):
    temp = float(msg.payload.decode())
    device_id = msg.topic.split("/")[-1]

    if device_id in isolated:
        print(f"IGNORED: {device_id} (ISOLATED)")
        return

    devices[device_id] = temp

    print(f"{device_id} Temperature: {temp}°C")

    if temp > 30:
        print(f"ALERT: temp abnormally high!")
        isolated.add(device_id)
        print(f"{device_id} has been isolated...")

client = mqtt.Client(
    client_id="Smart_Gateway",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_message = on_message

client.connect(mqttbroker, 1883, 60)
client.subscribe("TEMPERATURE/#")

client.loop_forever()

