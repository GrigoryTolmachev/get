#Калибровка давления

import numpy as np
import matplotlib.pyplot as plt
import textwrap as wrap
data = np.loadtxt("data_160.txt", dtype=int)
sr_arr1 = sum(data)/len(data)
#print(sr_arr1)
data = np.loadtxt("data_120.txt", dtype=int)
sr_arr2 = sum(data)/len(data)
#print(sr_arr2)
data = np.loadtxt("data_80.txt", dtype=int)
sr_arr3 = sum(data)/len(data)
#print(sr_arr3)
data = np.loadtxt("data_40.txt", dtype=int)
sr_arr4 = sum(data)/len(data)
#print(sr_arr4)
sr_arr=[sr_arr4,sr_arr3,sr_arr2,sr_arr1]
prs_arr=[40,80,120,160]
z=np.polyfit(prs_arr,sr_arr,0)

#График калибровки

fig, ax = plt.subplots(figsize=(3,3), dpi=200)
ax.plot(prs_arr,sr_arr,'royalblue',linestyle='solid',marker='h',markersize=0,markevery=0)
ax.legend('V(p)')
ax.set_title("\n".join(wrap.wrap("Калибровка давления")),loc='center')
plt.ylabel("Напряжение, В")
plt.xlabel("Давление, мм.рт.ст.")
plt.xlim(0,200)
plt.ylim(0,2000)
plt.minorticks_on()
plt.grid(which='major')
plt.grid(which='minor',linestyle=':')

plt.plot(prs_arr,sr_arr)
plt.show()
plt.savefig("Калибровка.svg")
#print(z)

#График давления в состоянии покоя

data = np.loadtxt("data_pokoy.txt", dtype=int)

fig, ax = plt.subplots(figsize=(3,3), dpi=200)
s=np.arange(len(data))
s=s*60/len(data)
ax.plot(s,data,'royalblue',linestyle='solid',marker='h',markersize=5,markevery=5000)
ax.legend('p(t)')
ax.set_title("\n".join(wrap.wrap("График давления в состоянии покоя")),loc='center')
plt.ylabel("Давление, мм.рт.ст.")
plt.xlabel("Время, с")
plt.xlim(0,60)
plt.ylim(90,170)
plt.minorticks_on()
plt.grid(which='major')
plt.grid(which='minor',linestyle=':')

#Калибровка

x=sr_arr1-sr_arr4
x/=120
x1=sr_arr4-40*x
x1=abs(x1)
x2=sr_arr3-80*x
x2=abs(x2)
x3=sr_arr2-120*x
x3=abs(x3)
x4=sr_arr1-160*x
x4=abs(x4)
y=x1+x2+x3+x4
y/=4

plt.plot(s,(data-y)/x)
plt.show()
plt.savefig("Давление в сост покоя.svg")

#Поиск диастолы

k=1800
for i in range(800000):
    if data[i]<k:
        k=data[i]
        m1=i
#print(round(60/len(data)*m1,2),round((k-y)/x,1))

#Поиск систолы

g=int((len(data)/60*20.7)//1)
k=0
for i in range(500000):
    if data[i+g]>k:
        k=data[i+g]
        m2=i+g
#print(round(60/len(data)*m2,2),round((k-y)/x,1))

#Нахождение значения пульса

u=[m2]
for i in data:
    data[i]=(data[i]-y)/x
k=1700
n1=0
for i in range(5000):
    if data[i+m2]<k:
        k=data[i+m2]
        n1=i+m2
#print(round(60/len(data)*n1,2),round((k-y)/x,1))
u.append(n1)

g=n1
i=0
while g<m1-5000:
    k = 0
    n1 = 0
    for i in range(5000):
        if data[i + g] > k:
            k = data[i + g]
            n1 = i + g
    u.append(n1)
    g=n1
    k = 1700
    n1 = 0
    for i in range(5000):
        if data[i + g] < k:
            k = data[i + g]
            n1 = i + g
    u.append(n1)
    g=n1
#print(len(u))
u[-1]=m1
#for i in range(len(u)):
    #print(round(60 / len(data) * u[i], 2),round((data[u[i]] - y) / x, 1))
print("В состоянии покоя давление:",round((data[u[0]] - y) / x, 1),'/',round((data[u[len(u)-1]] - y) / x, 1))
print("Пульс",round(len(u)*30/(round(60 / len(data) * u[-1], 2)-round(60 / len(data) * u[0], 2))),"ударов в минуту")

#Построение графика пульса

#print(u[0],u[1],data[u[0]]-(data[u[0]]+data[u[1]])/2)
for i in range(len(u)-1):
    for j in range(u[i+1]-u[i]-1):
        #print(data[u[i]],data[u[i+1]],data[j + u[i]],(data[u[i]]+data[u[i+1]])/2)
        data[1+j+u[i]]=data[1+j+u[i]]-(data[u[i]]+data[u[i+1]])/2
        #print(data[1+j+u[i]])

arrarr=[]
for i in range(u[-1]-u[0]):
    if data[i+u[0]]<100:
        arrarr.append(data[i+u[0]])
##print(arrarr)

fig, ax = plt.subplots(figsize=(3,3), dpi=200)
s=np.arange(len(arrarr))
s=s*(round(60 / len(data) * u[-1], 2)-round(60 / len(data) * u[0], 2))/len(arrarr)
ax.plot(s,arrarr/x,'royalblue',linestyle='solid',marker='h',markersize=0,markevery=0)
ax.legend('p(t)')
ax.set_title("\n".join(wrap.wrap("График пульса в состоянии покоя")),loc='center')
plt.ylabel("Изменение давления, мм.рт.ст.")
plt.xlabel("Время, с")
plt.xlim(0,32)
plt.ylim(-2.5,2.5)
plt.minorticks_on()
plt.grid(which='major')
plt.grid(which='minor',linestyle=':')

arrarr/=x
plt.plot(s,arrarr)
plt.show()
plt.savefig("Пульс в сост покоя.svg")
#print(s)
#print(arrarr/x)

#print(len(data))





# График давления после нагрузки

data = np.loadtxt("data_nagruz.txt", dtype=int)

fig, ax = plt.subplots(figsize=(3,3), dpi=200)
s=np.arange(len(data))
s=s*60/len(data)
ax.plot(s,data,'royalblue',linestyle='solid',marker='h',markersize=5,markevery=5000)
ax.legend('p(t)')
ax.set_title("\n".join(wrap.wrap("График давления после нагрузки")),loc='center')
plt.ylabel("Давление, мм.рт.ст.")
plt.xlabel("Время, с")
plt.xlim(0,60)
plt.ylim(90,170)
plt.minorticks_on()
plt.grid(which='major')
plt.grid(which='minor',linestyle=':')

# Калибровка

x=sr_arr1-sr_arr4
x/=120
x1=sr_arr4-40*x
x1=abs(x1)
x2=sr_arr3-80*x
x2=abs(x2)
x3=sr_arr2-120*x
x3=abs(x3)
x4=sr_arr1-160*x
x4=abs(x4)
y=x1+x2+x3+x4
y/=4

plt.plot(s,(data-y)/x)
plt.show()
plt.savefig("Давление после нагрузки.svg")

#Поиск диастолы

k=1800
for i in range(900000):
    if data[i+32000]<k:
        k=data[i+32000]
        m1=i+32000
#print(round(60/len(data)*m1,2),round((k-y)/x,1))

#Поиск систолы

g=int((len(data)/60*15.5)//1)
k=0
for i in range(500000):
    if data[i+g]>k:
        k=data[i+g]
        m2=i+g
#print(round(60/len(data)*m2,2),round((k-y)/x,1))

#Нахождение значения пульса

u=[m2]
for i in data:
    data[i]=(data[i]-y)/x
k=1700
n1=0
for i in range(5000):
    if data[i+m2]<k:
        k=data[i+m2]
        n1=i+m2
#print(round(60/len(data)*n1,2),round((k-y)/x,1))
u.append(n1)
g=n1
i=0
while g<m1-5000:
    k = 0
    n1 = 0
    for i in range(5000):
        if data[i + g] > k:
            k = data[i + g]
            n1 = i + g
    u.append(n1)
    g=n1
    k = 1700
    n1 = 0
    for i in range(5000):
        if data[i + g] < k:
            k = data[i + g]
            n1 = i + g
    u.append(n1)
    g=n1
#print(len(u))
u[-1]=m1
#for i in range(len(u)):
    #print(round(60 / len(data) * u[i], 2),round((data[u[i]] - y) / x, 1))
print("Давление после нагрузки:",round((data[u[0]] - y) / x, 1),'/',round((data[u[len(u)-1]] - y) / x, 1))
print("Пульс",round(len(u)*30/(round(60 / len(data) * u[-1], 2)-round(60 / len(data) * u[0], 2))),"удара в минуту")


#Построение графика пульса

for i in range(len(u)-1):
    for j in range(u[i+1]-u[i]-1):
        #print(data[u[i]],data[u[i+1]],data[j + u[i]],(data[u[i]]+data[u[i+1]])/2)
        data[1+j+u[i]]=data[1+j+u[i]]-(data[u[i]]+data[u[i+1]])/2
        #print(data[1+j+u[i]])

arrarr=[]
for i in range(u[-1]-u[0]):
    if data[i+u[0]]<100:
        arrarr.append(data[i+u[0]])
#print(arrarr)

fig, ax = plt.subplots(figsize=(3,3), dpi=200)
s=np.arange(len(arrarr))
s=s*(round(60 / len(data) * u[-1], 2)-round(60 / len(data) * u[0], 2))/len(arrarr)
ax.plot(s,arrarr/x,'royalblue',linestyle='solid',marker='h',markersize=0,markevery=0)
ax.legend('p(t)')
ax.set_title("\n".join(wrap.wrap("График пульса после нагрузки")),loc='center')
plt.ylabel("Изменение давления, мм.рт.ст.")
plt.xlabel("Время, с")
plt.xlim(0,44)
plt.ylim(-3.5,3.5)
plt.minorticks_on()
plt.grid(which='major')
plt.grid(which='minor',linestyle=':')

arrarr/=x
plt.plot(s,arrarr)
plt.show()
plt.savefig("Пульс после нагрузки.svg")
#print(s)
#print(arrarr/x)

#print(len(data))

