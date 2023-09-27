import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
p=GPIO.PWM(20,100)
p.start(0)
try:
    while (1):
        print("Введите целое число от 0 до 100")
        n=int(input())
        p.ChangeDutyCycle(n)
        print(round(n*3.3/100,2),'V')
finally:
    GPIO.output(20,0)
    GPIO.cleanup()