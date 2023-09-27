import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
dac=[8,11,7,1,0,5,12,6]
GPIO.setup(dac,GPIO.OUT)
def dec2bin(value):
    return [int (i) for i in bin(value)[2:].zfill(8)]
try:
    while(1):
        print("Введите целое число от 0 до 255")
        n=input()
        if n=='q':
            break
        else:
            n=int(n)
            GPIO.output(dac,dec2bin(n))
            print(round(n*3.3/256,2),'V')
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()