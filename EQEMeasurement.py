import csv
import statistics
import time
from PowerMeter import PowerMeter
from MonoChromater import MonoChromater
from pymeasure.instruments.keithley import Keithley2400
import SourceMeter as SM

#initializing values
currentPower = 0
currentCurrent = 0

wavelengths = []
eQEVals = []

i = 0


#reading in the bounds and step interval

lowerBound = int(input("Enter the lower bound for the range over which you'd like to measure the EQE, and press enter."))

upperBound = int(input("Enter the upper bound for the range over which you'd like to measure the EQE, and press enter."))

stepInt = float(input("Enter the step interval for the wavelength (i.e. if you'd like to measure every 5nm, enter 5). Note: the smaller the step, the longer you can expect the measurement to take."))




#reading in the instruments

thorLabs = PowerMeter('USB0::0x1313::0x8072::P2003101::0::INSTR', "thor labs")

keithley = Keithley2400('GPIB1::24::INSTR')

JV = MonoChromater('GPIB0::1::INSTR')


#writing headers into the file

with open('EQE_Data_6_17_new_2.csv', 'a') as csvFile:
    cwriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)


    cwriter.writerow(['wavlength','power (mW)','current (uA)','EQE'])

#measuring the values
#
# JV.prepForMeasurements(lowerBound)

for i in range(float(lowerBound),float(upperBound),float(stepInt)):



    thorLabs.setWavelength(i)

    print('measuring optical power')
    currentPower = thorLabs.measurePowerUntilSteady()

    print('measuring current:')
    stDev = 3.1
    data = []

    while(stDev>3):

        for j in range (0,5,1):
            data.append(SM.get_current(keithley))
            time.sleep(1)

        stDev = statistics.stdev((data))
        mean = statistics.mean(data)

        percentSTDV = (stDev/mean)*100

        if (stDev<3):
            currentCurrent = statistics.mean(data)
            print('current measurement steady!')
        else:
            print('current unsteady... remeasuring')

    print('Power for wavelength ' + str(i) + ': ' + str(currentPower))
    print('Current for wavelength ' + str(i) + ': ' + str(currentCurrent))

    #writing the value into the file

    currentRow = [str(i), currentPower, currentCurrent]

    with open('EQE_Data_6_17_new_2.csv', 'a') as csvFile:

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

    print('stepping up the wavelength to '+str(float(i)+float(stepInt))+" nanometers")
    JV.stepBy(stepInt)

    time.sleep(2)

print("complete!")


