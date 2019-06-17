import visa
import time
from MonoChromater import MonoChromater

rm = visa.ResourceManager()

MonoChromater = rm.open_resource('GPIB1::1::INSTR')

#
# for i in range(0, 10, 1):
#
#
#     MonoChromater.write('F0,1000')
#     MonoChromater.write('F0,0')
#
#     time.sleep(1.5)





mono = MonoChromater('GPIB1::1::INSTR','mono1')

mono.stepBy(-400)
