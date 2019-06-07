import visa
import pymeasure
from pymeasure.instruments.keithley import Keithley2400

''' The goal of this module is to provide methods for getting the measurement readings of a 
Keithley 2400 SourceMeter. The methods utilize the Keithley2400 class from PyMeasure.
'''

'Getters'
'Returns the present current reading'


def get_current(self):
    try:
        self.write(":CONFigure:CURRent")
        self.enable_source()
        self.measure_current()
        return self.current
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"


'Returns the present voltage reading'


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
        if (abs(self.voltage_level) > 210):
            print("Voltage out of range. The absolute limit is 210 V.")
            return "ERROR: OUT OF RANGE"
        self.apply_voltage()
        self.source_voltage = voltage_level
        self.enable_source()
    except:
        print("An error has occurred.\nPossible reason: method must take a Keithley2400 object")
        return "ERROR"

