import csv
import visa
import statistics
import time
from PowerMeter import PowerMeter
import pymeasure
from MonoChromater import MonoChromater
from SourceMeter import SourceMeter
from pymeasure.instruments.keithley import Keithley2400


#initializing values

currentPower = 0
currentCurrent = 0

rm = visa.ResourceManager()

wavelengths = []
eQEVals = []

i = 0


#reading in the bounds and step interval

initialize = input("On the monochromater software, set the first two slit widths to 3mm, and click move.\nThen set the wavelength to the lower bound of your wavelength sweep and press enter. \nWhen you've done this, press enter on your computer.")

lowerBound = input("Enter the lower bound for the range over which you'd like to measure the EQE, and press enter.")

upperBound = input("Enter the upper bound for the range over which you'd like to measure the EQE, and press enter.")

stepInt = input("Enter the step interval for the wavelength (i.e. if you'd like to measure every 5nm, enter 5). Note: the smaller the step, the longer you can expect the measurement to take.")




#reading in the instruments

thorLabs = PowerMeter('USB0::0x1313::0x8072::P2003101::0::INSTR', "thor labs")

keithley = Keithley2400('GPIB0::24::INSTR')

JV = MonoChromater('GPIB1::1::INSTR')


#writing headers into the file

with open('EQE_Data_Formatted.csv', 'a') as csvFile:
    cwriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)


    cwriter.writerow(['wavlength','power (mW)','current (uA)','EQE'])

#measuring the values

for i in range(int(lowerBound),int(upperBound),stepInt):

    thorLabs.setWavelength(i)

    print('measuring optical power')
    currentPower = thorLabs.measurePowerUntilSteady()

    print('measuring current:')
    stDev = 3.1
    data = []

    while(stDev>3):

        for j in range (0,5,1):
            data.append(keithley.current)
            time.sleep(1)

        stDev = statistics.stdev(data)/statistics.mean(data)*100

        if (stDev<3):
            currentCurrent = statistics.mean(data)
            print('current measurement steady!')
        else:
            print('current unsteady... remeasuring')

    print('Power for wavelength ' + str(i) + ': ' + str(currentPower))
    print('Current for wavelength ' + str(i) + ': ' + str(currentCurrent))

    #writing the value into the file

    currentRow = [str(i), currentPower, currentCurrent]

    with open('EQE_Data.csv', 'a') as csvFile:

        cwriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        wavelength = int(i)
        formattedPower = round(1000*currentPower,3)
        formattedCurrent = round(1000000*currentCurrent,11)

        wavelengths.append(wavelength)

        if (formattedCurrent == 0):
            currentByPower = 0
        else:
            currentByPower = formattedCurrent/(formattedPower*1000)

        eQE = 100 * (10**(9) * 1.24*10**(-6) * currentByPower) / float(wavelength)

        eQE = round(eQE,1)

        eQEVals.append((eQE))

        currentRow = [int(i), formattedPower, formattedCurrent, eQE]

        cwriter.writerow(currentRow)


    #stepping up the mono before the next reading

    print('stepping up the wavelength to '+str(int(i)+int(stepInt))+" nanometers")
    JV.stepBy(stepInt)

    time.sleep(2)



print(wavelengths)
print(eQEVals)

