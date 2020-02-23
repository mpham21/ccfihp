from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
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
        self.mqtt_client = self._init_mqtt_client()

    # Function to connect and subscribe MQTT client
    def mqtt_connect(self):
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

    # Function to be called on message receiving message
    @abstractmethod
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

