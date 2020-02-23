"""
This script emulates a temperature sensor sending data to AWS IoT Core using AWS IoT Python SDK. Messages are
transmitted using MQTT client.

Date of creation: 28/01/2020
Author: Matthew Pham
Employee number: 530259
"""

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import random

# Disable collection of metrics from MQTT Client
# AWSIoTMQTTClient.disableMetricsCollection()

# Device specific data
thing_name = "infosys_computer"
endpoint = "arwvlqj3bmcqg-ats.iot.us-east-2.amazonaws.com"

# Assign locations of certificates and keys
root_cert = r"certs/root-CA.crt"
private_key = r"certs/" + thing_name + ".private.key"
public_key = r"certs/" + thing_name + ".public.key"
policy = r"certs/" + thing_name + ".cert.pem"

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient(thing_name)

# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint(endpoint, 8883)
myMQTTClient.configureCredentials(root_cert, private_key, policy)
myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


# Custom MQTT message callback
def custom_callback(client, userdata, message):
    global device_on

    print(f"message received from: {message.topic}")
    if message.topic == "health_tracker/cmd_stream":
        json_obj = json.loads(message.payload)
        device_on = json_obj["device_on"]
        if device_on:
            print("device has been turned ON\n")
        else:
            print("device has been turned OFF\n")
        print("--------------\n")
    elif message.topic == "trigger_scenario":
        code_red()


device_on = False
sensor_data = {
    "heart_rate": 60,
    "steps": 0,
    "calories_burnt": 0,
}


def code_red():
    print("RED ALERT TRIGGERED")
    global sensor_data, device_on
    sensor_data["heart_rate"] = 150
    device_on = True


pub_topic = "health_tracker/dt_stream"
sub_topic = ["health_tracker/cmd_stream", "trigger_scenario"]
# Connect and subscribe to AWS IoT
myMQTTClient.connect()

for topic in sub_topic:
    myMQTTClient.subscribe(topic, 1, custom_callback)

# Publish to the same topic in a loop forever
while True:
    if device_on:
        messageJson = json.dumps(sensor_data)
        myMQTTClient.publish(pub_topic, messageJson, 1)
        print('Published topic %s: %s\n' % (pub_topic, messageJson))

        # update sensor data
        sensor_data["heart_rate"] = random.randint(60, 80)
        sensor_data["steps"] += random.randint(0, 10)
        sensor_data["calories_burnt"] = sensor_data["steps"]//100
    else:
        print("idle...\n")
    time.sleep(5)
