
def on_message(client, userdata, msg):
    temp = float(msg.payload.decode())

    print(f"{temp}")

    if temp > 30:
        print(f"ALERT: temp abnormally high")
