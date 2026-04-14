import paho.mqtt.client as mqtt
from smart_gateway import on_message

mqttbroker = "broker.hivemq.com"

client = mqtt.Client(
    cliend_id="Smart_Gateway",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_message = on_message

client.connect(mqttbroker, 1883, 60)
client.subscribe("TEMPERATURE")

client.loop_forever()