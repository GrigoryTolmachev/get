import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(16,GPIO.IN)
GPIO.output(17,GPIO.input(16))