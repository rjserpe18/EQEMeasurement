import csv
import visa
import statistics
import time
from PowerMeter import PowerMeter
import pymeasure
from MonoChromater import MonoChromater
import SourceMeter

from pymeasure.instruments.keithley import Keithley2400
import SourceMeter as SM


currentPower = 0
currentCurrent = 0
stepInt = 5 * 32

'''
initialize = input("On the monochromater software, set the first two slit widths to 3mm, and click move.\nThen set the wavelength to the lower bound of your wavelength sweep and press enter. \nWhen you've done this, type '1' and press enter.  ")

lowerBound = input("Enter the lower bound for the range over which you'd like to measure the EQE, and press enter.")

upperBound = input("Enter the upper bound for the range over which you'd like to measure the EQE, and press enter.")

step = input("Enter the step interval for the wavelength (i.e. if you'd like to measure every 5nm, enter 5). Note: the smaller the step, the longer you can expect the measurement to take.")
'''

#reading in the instruments

rm = visa.ResourceManager()


thorLabs = PowerMeter('USB0::0x1313::0x8072::P2003101::0::INSTR', "thor labs")

keithley = Keithley2400('GPIB0::24::INSTR')






MonoChromater = rm.open_resource('GPIB0::1::INSTR')


#
#measuring the values

for i in range(350,800,20):

    thorLabs.setWavelength(i)

    print(SM.get_current(keithley))
    currentPower = thorLabs.measurePowerUntilSteady()


    currentCurrent = SM.get_current(keithley)

    #writing the value into the file

    currentRow = [str(i), currentPower, currentCurrent]

    with open('EQE_Data.csv', 'a') as csvFile:
        cwriter = csv.writer(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        cwriter.writerow(currentRow)





    MonoChromater.write("F0,"+str(stepInt))
    time.sleep(5)




