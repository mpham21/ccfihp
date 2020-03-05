from skeleton_device.skeleton_device import IoTDevice
import json
from gpiozero import Servo
from time import sleep



class MedicationDispenser(IoTDevice):
    def __init__(self, thing_name, host, pub_topic, sub_topic, device_data, servo_pin):
        super().__init__(thing_name, host, pub_topic, sub_topic, device_data)
        self.servo = Servo(servo_pin)
        self.servo.min()

    def custom_callback(self, client, userdata, message):
        print(f"message received from: {message.topic}")
        self.dispense_meds(2)
        return

    def dispense_meds(self, dosage):
        for _ in range(dosage):
            self.servo.min()
            sleep(1)
            self.servo.max()
            sleep(1)
            self.servo.min()
            print("dispensed")
    
    

thing_name = "medication_dispenser"
endpoint = "arwvlqj3bmcqg-ats.iot.us-east-2.amazonaws.com"
dispenser_data =  {
    "patient_info": {
        "patient_id": "P1382A"
        },
    "device_info": {
        "type": "medication dispenser",
        "firmware": "4.1.5"
        },
    "contextual_info": {
        "timestamp": None,
        "location": None
        },
    "message": {
        "type": "paracetamol",
        "quantity": 10,
        "expiry_date": "2020-01-01T00:00:00"
        }

    }


pub_topic = "medication_dispenser/dt_stream"
sub_topic = ["medication_dispenser/cmd_stream"]
servo_pin = 24

device = MedicationDispenser(thing_name, endpoint, pub_topic, sub_topic, dispenser_data, servo_pin)


device.main()






