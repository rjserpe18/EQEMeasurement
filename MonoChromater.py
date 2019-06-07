import visa
import pymeasure
import time

rm = visa.ResourceManager()

MonoChromater = rm.open_resource('GPIB0::1::INSTR')

#i3 -- slit with output light

#32 steps changes by 1 nanometer
#it also waits up on the command
#to get something to move the way you want it to, just precede it by the zero command


MonoChromater.write("F0,1000")
MonoChromater.write("F0,0")

time.sleep(5)

MonoChromater.write("F0,-1000")
MonoChromater.write("F0,0")






'''

512.50
509.38
506.25
503.13
500





print("initializing the motor")
time.sleep(10)

MonoChromater.write('i0,3,0')

print("initializing the slit ")
time.sleep(10)


MonoChromater.write("g0,3,5000")


print("setting the speed")
time.sleep(10)


MonoChromater.write('k0,3,1000')


print("opening the front slit")
'''

#
# print(MonoChromater.write("g0,0,400"))
#
#
# print(MonoChromater.write("k0,1,-500"))





# print(MonoChromater.write(" "))
#
#
# print(MonoChromater.write("MOTOR MOVE RELATIVE"))
#
# print(MonoChromater.write("MOTOR READ POSITION"))
#
# print(MonoChromater.query("MOTOR READ POSITION"))


