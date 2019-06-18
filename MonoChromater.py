import visa
import pymeasure
import time
from PowerMeter import PowerMeter



#32 steps changes by 1 nanometer
#it also waits up on the command
#to get something to move the way you want it to, just place the zero move command after it


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

        self.mono.write("F0,"+str(amountToStep))
        self.mono.write("F0,0")



    def isBusy(self):

        while(self.mono.write('E') == 'o'):
            return True
            print('waiting on motor movement')
            time.sleep(2)
        return False



    def openSlits(self):
        for i in range(0, 3, 1):
            self.mono.write("k0,2,500")
            self.mono.write('k0,2,0')
            print('moving motor 2')
            time.sleep(3)

        time.sleep(2)

        # while(self.isBusy()):
        #     time.sleep(.1)

        for i in range(0, 3, 1):
            self.mono.write("k0,0,500")
            self.mono.write('k0,0,0')
            print('moving motor 0')
            time.sleep(3)

        # while (self.isBusy()):
        #     time.sleep(.1)

        print("slits opened!")

    #method that opens the slits, sets to the initial wavelength
    def prepForMeasurements(self, startingPosition):

        self.mono.write('A')

        print('waiting on initialization')
        time.sleep(30)

        print('moving motor to initial position')
        self.stepBy(-(1100-startingPosition))

        time.sleep(10)

        print('opening slits')
        self.openSlits()
        time.sleep(3)


        print("ready for measurements!")

