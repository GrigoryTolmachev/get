import numpy as np
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

#def k_finder(v,v0 , h):  # эта функция определяет коэф k, определяющий зависимость напряжения от глубины v = v0 + k*h
#    #ожидаемо, к < 0
#    return (v - v0)  / h

def binary(n):  # перевод в двоичную сс
    return [int(i) for i in bin(n)[2:].zfill(8)]


def adc():  # ацп
    value = 0
    for i in range(7, -1, -1):
        value += 2 ** i
        GPIO.output(dac, binary(value))
        time.sleep(0.0005)
        if GPIO.input(comp) == 1:
            value -= 2 ** i
    return value

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(21, GPIO.IN)
listADC = []  # напряжение
data = []


while True:  # отслеживает открытие крышки слива
    print(GPIO.input(21), "- состояние закрывашки")
    if GPIO.input(21) == 1:
        timeStart = time.time()
        break

print('BEGIN')

while True:  # снимает напряжение с ацп и время
    time.sleep(0.005)
    listADC.append(str(adc()))
    data.append([time.time() - timeStart, adc()])
    if time.time() - timeStart > 15:
        break

with open("value_104.txt",'w') as f:
    f.write("\n".join(listADC))
print("END")
