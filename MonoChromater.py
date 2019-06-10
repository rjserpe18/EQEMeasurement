import visa
import pymeasure
import time

rm = visa.ResourceManager()




MonoChromater = rm.open_resource('GPIB1::1::INSTR')

for i in range (0,5,1):
    MonoChromater.write('F0,640')
    time.sleep(2)


#i3 -- slit with output light

#32 steps changes by 1 nanometer
#it also waits up on the command
#to get something to move the way you want it to, just precede it by the zero command



#steps the monochromater ahead by the desired number of nanometers


class MonoChromater:

    def stepBy(nanometers):
        amountToStep = 32*nanometers
        MonoChromater.write("F0,"+str(amountToStep))

