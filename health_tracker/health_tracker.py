from skeleton_device.skeleton_device import IoTDevice
import json
import random
import time

class HealthTracker(IoTDevice):
    # callback to be called when message received from a subscribed topic
    def custom_callback(self, client, userdata, message):
        print("message received from: "+ message.topic)
        
        # command stream message handling
        if message.topic == "health_tracker/cmd_stream":
            json_obj = json.loads(message.payload)
            if isinstance(json_obj["device_on"], bool):
                self.device_data["message"]["device_on"] = json_obj["device_on"]
            if self.device_data["message"]["device_on"]:
                print("device has been turned ON\n")
            else:
                print("device has been turned OFF\n")
            print("--------------\n")
            
        # trigger increased heart rate scenario
        elif message.topic == "trigger_scenario":
            self.code_red()
    
    # main function
    def main(self):
        self.mqtt_connect()

        while True:
            if self.device_data["message"]["device_on"]:
                self.telemetry()
                self.update_data()
            else:
                print("Idle...")
            time.sleep(5)
                               
    def update_data(self):
        # update sensor data
        self.device_data["contextual_info"]["timestamp"] = time.time()
        self.device_data["message"]["heart_rate"] = random.randint(60, 80)
        self.device_data["message"]["steps"] += random.randint(0, 10)
        self.device_data["message"]["calories_burnt"] = self.device_data["message"]["steps"] // 100

    def code_red(self):
        print("RED ALERT TRIGGERED")
        self.device_data["message"]["heart_rate"] = 150
        self.device_data["message"]["device_on"] = True
    
# setting device values
device_name = "infosys_computer"
host = "arwvlqj3bmcqg-ats.iot.us-east-2.amazonaws.com"
pub_topic = "health_tracker/dt_stream"
sub_topic = ["health_tracker/cmd_stream", "trigger_scenario"]
device_data = {
    "patient_info": {
        "patient_id": "P1382A"
        },
    "device_info": {
        "type": "smart watch",
        "firmware": "4.1.5"
        },
    "contextual_info": {
        "timestamp": None,
        "location": None
        },
    "message": {
            "device_on": True,
            "heart_rate": 60,
            "steps": 0,
            "calories_burnt": 0,
        }
    }

# initialising device
device = HealthTracker(device_name, host, pub_topic, sub_topic, device_data)
# activating device
device.main()

