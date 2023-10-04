import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac=[8,11,7,1,0,5,12,6]
comp=14
troyka=13
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT,initial=1)
GPIO.setup(comp,GPIO.IN)
def dec2bin(value):
    return [int (i) for i in bin(value)[2:].zfill(8)]
def adc():
    i=128
    k=0
    for j in range(8):
        GPIO.output(dac,dec2bin(i+k))
        time.sleep(0.07)
        if GPIO.input(comp)==0:
            k+=i
        i=i//2
    return(k)
try:
    while(1):
        n=adc()
        print(round(n*3.3/256,2),"V ",n)

finally:
    GPIO.output(dac,0)
    GPIO.output(troyka,0)
    GPIO.cleanup()