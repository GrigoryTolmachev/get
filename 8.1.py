import numpy as np
import matplotlib.pyplot as plt
import textwrap as wrap
with open("settings.txt",'r') as settings:
    tmp = [float(i) for i in settings.read().split("\n")]

data = np.loadtxt("data.txt", dtype=int)
data=tmp[0]*data
fig, ax = plt.subplots(figsize=(5,5), dpi=200)
s=np.arange(len(data))
s=tmp[1]*s
ax.plot(s,data,'g',linestyle='solid',marker='h',markersize=5,markevery=50)
ax.legend('V(t)')
ax.set_title("\n".join(wrap.wrap("Заряд и разрядка конденсатора в RC-цепи Заряд и разрядка конденсатора в RC-цепи Заряд и разрядка конденсатора в RC-цепи")),loc='center')
plt.ylabel("Напряжение, B")
plt.xlabel("Время, с")
plt.xlim(0,10)
plt.ylim(0,round(0.2+max(data),1))
plt.minorticks_on()
plt.grid(which='major')
plt.grid(which='minor',linestyle=':')
plt.text(5,3,"время заряда =")
plt.text(9,3,"c")
plt.text(8,3,round(tmp[1]*np.argmax(data),2))
plt.text(5,2.5,"время разряда =")
plt.text(9.2,2.5,"c")
plt.text(8.2,2.5,round(s[-1]-tmp[1]*np.argmax(data),2))
plt.show()
print(tmp,ax,max(data))
fig.savefig("plot.svg")