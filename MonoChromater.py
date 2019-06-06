import visa
import pymeasure

rm = visa.ResourceManager()
print(rm.list_resources())

MonoChromater = rm.open_resource('GPIB0::1::INSTR')


print(MonoChromater.write("g0,0,400"))

print(MonoChromater.write("k0,1,-500"))



#make sure to delay for 100 seconds after waking up computer



#
#
# print(MonoChromater.write(" "))
#
#
# print(MonoChromater.write("MOTOR MOVE RELATIVE"))
#
# print(MonoChromater.write("MOTOR READ POSITION"))
#
# print(MonoChromater.query("MOTOR READ POSITION"))


