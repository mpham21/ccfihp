from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, AWSIoTMQTTShadowClient
import json
import time
from abc import ABC, abstractmethod


class IoTDevice(ABC):
    def __init__(self, thing_name, host, pub_topic, sub_topic, device_data):
        self.thing_name = thing_name
        self.host = host
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.device_data = device_data


    # Function to connect and subscribe MQTT client
    def mqtt_connect(self):
        self.mqtt_client = self._init_mqtt_client()
        self.mqtt_client.connect()

        for topic in self.sub_topic:
            self.mqtt_client.subscribe(topic, 1, self.custom_callback)

    # Returns MQTT client
    def _init_mqtt_client(self):
        # Assign locations of certificates and keys
        root_cert = r"certs/root-CA.crt"
        private_key = r"certs/" + self.thing_name + ".private.key"
        public_key = r"certs/" + self.thing_name + ".public.key"
        policy = r"certs/" + self.thing_name + ".cert.pem"

        # For certificate based connection
        my_mqtt_client = AWSIoTMQTTClient(self.thing_name)

        # Configurations
        # For TLS mutual authentication
        my_mqtt_client.configureEndpoint(self.host, 8883)
        my_mqtt_client.configureCredentials(root_cert, private_key, policy)
        my_mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
        my_mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        my_mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
        my_mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
        my_mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

        return my_mqtt_client

    # Function to connect and subscribe MQTT client
    def shadow_connect(self):
        self.shadow_client = self._init_shadow_client()
        self.shadow_client.connect()

        self.device_shadow_handler = self.shadow_client.createShadowHandlerWithName(self.thing_name, True)

    # Returns MQTT client
    def _init_shadow_client(self):
        # Assign locations of certificates and keys
        root_cert = r"certs/root-CA.crt"
        private_key = r"certs/" + self.thing_name + ".private.key"
        public_key = r"certs/" + self.thing_name + ".public.key"
        policy = r"certs/" + self.thing_name + ".cert.pem"

        # For certificate based connection
        my_shadow_client = AWSIoTMQTTShadowClient(self.thing_name)

        # Configurations
        # For TLS mutual authentication
        my_shadow_client.configureEndpoint(self.host, 8883)
        my_shadow_client.configureCredentials(root_cert, private_key, policy)
        my_shadow_client.configureAutoReconnectBackoffTime(1, 32, 20)
        my_shadow_client.configureConnectDisconnectTimeout(10)  # 10 sec
        my_shadow_client.configureMQTTOperationTimeout(5)  # 5 sec

        return my_shadow_client

    def update_shadow_state(self, state):
        self.device_shadow_handler.shadowUpdate(state, self.custom_shadow_callback_update, 5)

    # Custom Shadow callback
    def custom_shadow_callback_update(payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
        if responseStatus == "accepted":
            payloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Update request with token: " + token + " accepted!")
            print("property: " + str(payloadDict["state"]["desired"]["property"]))
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Update request " + token + " rejected!")
    # Function to be called on message receiving message

    def custom_callback(self, client, userdata, message):
        print(f"Message received from {message.topic}: {message.payload}")

    # Function to relay device data to IoT Core
    def telemetry(self):
        message_json = json.dumps(self.device_data)
        self.mqtt_client.publish(self.pub_topic, message_json, 1)
        print("Published topic %s: %s\n" % (self.pub_topic, message_json))

    # Function to update device data
    def update_data(self):
        pass

    # main function for run time execution
    def main(self):
        self.mqtt_connect()

        while True:
            self.telemetry()
            self.update_data()
            time.sleep(5)

