from skeleton_device.skeleton_device import IoTDevice
import json
import time
import RPi.GPIO as GPIO

class Heart(IoTDevice):
    def custom_callback(self, client, userdata, message):
        payload = json.loads(message.payload)
        self.device_data["heart_rate"] = payload["message"]["heart_rate"]
        self.heart_rate = self.device_data["heart_rate"]
        print(f"Current heart rate: {self.heart_rate}")

    def main(self):
        self.mqtt_connect()
        self.heart_rate = 60
        self.init_GPIO()
        self.button_down = True
        while True:
            beat_length = 0.2
            beat_interval = (60 - self.heart_rate * beat_length)/self.heart_rate
            GPIO.output(self.red_pin, GPIO.HIGH)
            time.sleep(beat_length)
            GPIO.output(self.red_pin, GPIO.LOW)
            time.sleep(beat_interval)

            pass
    
    def init_GPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.button_pin = 12
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.button_callback)

        bpm = 100
        self.red_pin = 16
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.output(self.red_pin, GPIO.LOW)
        

    def button_callback(self, channel):
        if self.button_down == True:
            self.heart_rate = 150
            message_json = json.dumps(self.device_data)
            self.mqtt_client.publish(self.pub_topic, message_json, 1)
            print("Published topic %s: %s\n" % (self.pub_topic, message_json))
        else:
            self.button_down = True
    

device_name = "heart"
host = "arwvlqj3bmcqg-ats.iot.us-east-2.amazonaws.com"
pub_topic = "trigger_scenario"
sub_topic = ["health_tracker/dt_stream", "sdk/test/Python"]
device_data = {
            "heart_rate": 60
        }

device = Heart(device_name, host, pub_topic, sub_topic, device_data)
device.main()

