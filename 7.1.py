import RPi.GPIO as  GPIO
import time
import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)
leds=[2,3,4,17,27,10,9]
dac=[8,11,7,1,0,5,12,6]
comp=14
troyka=13
GPIO.setup(leds,GPIO.OUT)
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT)
GPIO.setup(comp,GPIO.IN)

# Описание функций
def dec2bin(value):
    return [int (i) for i in bin(value)[2:].zfill(8)]
def adc():
    i=128
    k=0
    for j in range(8):
        GPIO.output(dac,dec2bin(i+k))
        time.sleep(0.003)
        if GPIO.input(comp)==0:
            k+=i
        i=i//2
    return(k)


# Описание переменных
s=[]
t=time.time()


try:
    GPIO.output(troyka,1)
    while(1):
        # Зарядка конденсатора
        n=adc()
        print(n)
        s.append(n)
        if adc()>204:
            break

    # Разрядка конденсатора
    GPIO.output(troyka,0)
    while(1):
        n=adc()
        print(n)
        s.append(n)
        if adc()<193:
            break


    t=time.time()-t # Расчет времени
    plt.plot(s) 
    plt.show()      # Построение графика
    tme=0
    for i in s:
        tme+=1

    # Вывод основных значений
    print("Продолжительность эксперимента",round(t,1),"с")
    print("Период",round(t/tme,3),"с")
    print("частота дискретизации",round(tme/t,1),"Гц")
    print("Шаг квантования",round(3.3/256,3),"В")
    sstr=[str(i) for i in s]

    
    # Запись данных в файлы
    with open("data.txt", "w") as outfile:
        outfile.write("\n".join(sstr))
    with open("settings.txt", "w") as file:
        file.write(str(round(tme/t,1)))
        file.write("\n")
        file.write(str(round(3.3/256,3)))


finally:
    # Сброс настроек
    GPIO.output(leds,0)
    GPIO.output(dac,0)
    GPIO.output(troyka,0)
    GPIO.cleanup()