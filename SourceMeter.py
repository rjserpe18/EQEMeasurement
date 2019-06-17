import visa
import pymeasure
import statistics
import time
from pymeasure.instruments.keithley import Keithley2400

''' The goal of this module is to provide methods for getting the measurement readings of a 
Keithley 2400 SourceMeter. The methods utilize the Keithley2400 class from PyMeasure.

'''


class SourceMeter:

    def measureCurrentUntilSteady(meter):

        def deviationIsSteady(deviation):
            while (deviation > 1):
                return False
            return True

        def percentSTDV(dataSet):
            return 100 * statistics.stdev(dataSet) / statistics.mean(dataSet)

        data = []

        i = 1

        deviation = 1.1

        while (deviationIsSteady(deviation) == False):

            print("")
            print("trial " + str(i))

            data = []

            print("measuring values")
            for j in range(1, 6, 1):
                data.append(keithley.current)
                time.sleep(1)

            print("assessing data stability...")
            time.sleep(.5)

            deviation = percentSTDV(data)
            print("stdv for trial " + str(i) + ": " + str(deviation))

            print("data set for trial " + str(i) + ":" + str(data))

            if (deviation > 1):
                print("data unsteady. remeasuring....")
            else:
                print("data steady!")
                print(statistics.mean(data))
                toReturn = statistics.mean(data)

            i += 1

        return toReturn

def get_current(self):
    try:
        self.write("CONFigure:CURRent")
        self.measure_current()
        return self.current
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"

def get_voltage(self):
    try:
        self.write(":CONFigure:VOLTage")
        self.measure_voltage()
        return self.voltage
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"


'Returns the present resistance reading'

def get_resistance(self):
    try:
        self.write(":CONFigure:RESIstance")
        self.measure_resistance()
        if self.resistance < 0:
            return "Warning! Possible overflow: " + self.resistance
        else:
            return self.resistance
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"

'Setters'
'None of these enable the output. This can be done with the self.enable_output() command Keithley2400'
'Set output current'
def set_output_current(self, current_level):
    try:
        if (abs(current_level) > 1.05):
            print("Current out of range. The absolute limit is 1.05A.")
            return "ERROR: OUT OF RANGE"
        else:
            self.apply_current()
            self.source_current = current_level
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"

'Set output voltage'
def set_output_voltage(self, voltage_level):
    try:
        if (abs(voltage_level) > 210):
            print("Voltage out of range. The absolute limit is 210 V.")
            return "ERROR: OUT OF RANGE"
        self.apply_voltage()
        self.source_voltage = voltage_level
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"

'Zero all sources'
def zero_sources(self):
    try:
        set_output_current(self, 0)
        set_output_voltage(self, 0)
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"


rm = visa.ResourceManager()
print(rm.list_resources())

keithley = Keithley2400('GPIB1::24::INSTR')

print(keithley.current)

print(keithley.compliance_current)