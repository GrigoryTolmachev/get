import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac=[8,11,7,1,0,5,12,6]
GPIO.setup(dac,GPIO.OUT)
def dec2bin(value):
    return [int (i) for i in bin(value)[2:].zfill(8)]
try:
    n=0
    print("Введите период в секундах")
    t=int(input())
    while(1):
        while(n<255):
            n+=1
            GPIO.output(dac,dec2bin(n))
            time.sleep(t/510)
        while(n>0):
            n-=1
            GPIO.output(dac,dec2bin(n))
            time.sleep(t/510)
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()