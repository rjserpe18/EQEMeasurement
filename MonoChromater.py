import visa
import pymeasure
import time
from PowerMeter import PowerMeter



#i3 -- slit with output light

#32 steps changes by 1 nanometer
#it also waits up on the command
#to get something to move the way you want it to, just precede it by the zero command



#steps the monochromater ahead by the desired number of nanometers


class MonoChromater:

    def __init__(self, address):



        rm = visa.ResourceManager()

        monochromater = rm.open_resource(address)

        self.resourceManager = rm
        self.mono = monochromater
        self.address = address



    def stepBy(self,nanometers):
        amountToStep = 32*nanometers

        self.mono.write("F0,0")
        self.mono.write("F0,"+str(amountToStep))
        self.mono.write("F0,0")

    #method that opens the slits, sets the initial wavelength
    def prepForMeasurements(self,keithley):

        self.mono.write('A')

        while( self.mono.query('yes') == '2'):
            return 2




#lamp slit is #0
#beam slit is #2


rm = visa.ResourceManager()

JV = MonoChromater('GPIB0::1::INSTR')

#
# JV.mono.write("A")
#
# input('enter')
#
# JV.mono.write("k0,2,500")
# JV.mono.write('k0,2,0')

# #
# input('enter')
#
JV.stepBy(40)


#
# JV.mono.write('F0,-1000')
# JV.mono.write('F0,0')
#


