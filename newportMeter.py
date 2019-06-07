import visa
import time
import matplotlib.pyplot as plt

from PowerMeter import PowerMeter
import pymeasure

rm = visa.ResourceManager()

powerMeter = rm.open_resource("USB0::0x1313::0x8072::P2003101::0::INSTR")

powerMeter.write('sense:corr:wav 638')

'''

data = []
angles = []

for i in range(0,21,2):
    angles.append(i)

data = [4.13669186,4.08882013,4.15188901,4.55917499,4.92390885,4.77497582,4.68759215,4.66555648,4.71114821,4.67923324,4.6374416]

plt.plot(angles, data)
plt.grid()
plt.xlabel('Angles (degrees)')
plt.ylabel('Power (10^-4 W)')
plt.title('Power vs Incident Angle')
plt.show()




'''


j = -20


data = []
angles = []


while j<=20:

    print(j)
    print(powerMeter.query('measure:power?'))
    data.append(powerMeter.query('measure:power?'))
    time.sleep(20)
    j+=2


print(data)







