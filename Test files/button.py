import time
import RPi.GPIO as GPIO
import os
counter = 20

        
      
def button_callback(channel):
    for _ in range(10): print()
    global counter
    print(f"Button was pressed {counter} times")
    counter += 1

def heartbeat(length):
    first_thump = beat_interval * 0.1
    second_thump = beat_interval * 0.1
    middle_gap = beat_interval * 0.1
    trailing_gap = beat_interval * 0.6
    GPIO.output(red_pin, GPIO.HIGH)
    time.sleep(first_thump)
    GPIO.output(red_pin, GPIO.LOW)
    time.sleep(middle_gap)
    GPIO.output(red_pin,GPIO.HIGH)
    time.sleep(second_thump)
    GPIO.output(red_pin, GPIO.LOW)
    time.sleep(trailing_gap)
    
    

    

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
button_pin = 12
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback)

bpm = 100
red_pin = 16
GPIO.setup(red_pin, GPIO.OUT)
GPIO.output(red_pin, GPIO.LOW)

beat_length = 0.2
while True:
    beat_interval = (60 - counter * beat_length)/counter
    GPIO.output(red_pin, GPIO.HIGH)
    time.sleep(beat_length)
    GPIO.output(red_pin, GPIO.LOW)
    time.sleep(beat_interval)
    


