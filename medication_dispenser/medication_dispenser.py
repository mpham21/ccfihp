"""
This script emulates a temperature sensor sending data to AWS IoT Core using AWS IoT Python SDK. Messages are
transmitted using MQTT client.

Date of creation: 28/01/2020
Author: Matthew Pham
Employee number: 530259
"""

from skeleton_device import IoTDevice
import json


class MedicationDispenser(IoTDevice):

    def custom_callback(self, client, userdata, message):
        print(f"message received from: {message.topic}")
        try:
            json_obj = json.loads(message.payload)
            """
                message will be in the form:
                {
                    type: String,
                    quantity: int 
                }
            """
            dispensed = False
            for slot in dispenser_data.keys():
                medication = dispenser_data[slot]
                if medication["type"] == json_obj["type"]:
                    if medication["quantity"] - json_obj["quantity"] >= 0:
                        medication["quantity"] -= json_obj["quantity"]
                        print(f'{json_obj["quantity"]} dose/s of {json_obj["type"]} was dispensed')
                    else:
                        print(
                            f'requested dosage of {json_obj["quantity"]} {json_obj["type"]} exceeded dosage on hand ({medication["quantity"]})')
                    dispensed = True
            if not dispensed:
                print(f'{json_obj["type"]} was not found in dispenser')
        except:
            print("Invalid message")

thing_name = "medication_dispenser"
endpoint = "arwvlqj3bmcqg-ats.iot.us-east-2.amazonaws.com"
dispenser_data = {
    "slot_1": {
        "type": "ibuprofen",
        "quantity": 10,
        "expiry_date": "2020-08-01T00:00:00"
    },
    "slot_2": {
        "type": "paracetamol",
        "quantity": 10,
        "expiry_date": "2020-01-01T00:00:00"
    }
}
pub_topic = "medication_dispenser/dt_stream"
sub_topic = ["medication_dispenser/cmd_stream"]

device = MedicationDispenser(thing_name, endpoint, pub_topic, sub_topic, dispenser_data)
device.main()






