import RPi.GPIO as GPIO
from time import sleep
from threading import Thread, Event

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT, initial = GPIO.LOW)

def relay_activate():
    while True:
        event.wait()
        while event.is_set():
            GPIO.output(23, GPIO.HIGH)
            sleep(1)
            GPIO.output(23, GPIO.LOW)
            sleep(1)

event = Event()
Thread(target=relay_activate).start()