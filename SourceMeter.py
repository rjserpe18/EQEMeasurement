import visa
import pymeasure
from pymeasure.instruments.keithley import Keithley2400

''' The goal of this module is to provide methods to communicate with a Keithley 2400 Sourcemeter.
The module has methods for:
1. Getting the current machine measurement
2. Setting the type and parameters of measurement
3. Performing sweeps of measurements
The methods utilize the Keithley2400 class from PyMeasure. A standalone class was not created
'''

'Getters'
def get_current(self):
    try:
        self.write(":CONFigure:CURRent")
        self.enable_source()
        self.measure_current()
        return self.current
    except:
        return "An error has occurred.\nPossible reason: method must take a Keithley2400 object"
'Returns the present current reading'
'''
'Returns the present voltage reading'
def get_voltage(self):
    try:
        self.measure_voltage()
        return self.voltage
    except:
        return "An error has occurred.\nPossible reason: method must take a Keithley2400 object"


'Returns the present resistance reading'
def get_resistance(self):
    try:
        self.measure_resistance()
        return self.resistance
    except:
        return "An error has occurred.\nPossible reason: method must take a Keithley2400 object"

'Setters'

'Set output current'
def set_output_current(self, current_level):
    try:
        self.apply_current()
        self.source_current = current_level
        self.enable_source()
    except:
        return "An error has occurred.\nPossible reason: method must take a Keithley2400 object"

'Set output voltage'
def set_output_voltage(self, voltage_level):
    try:
        self.apply_voltage()
        self.source_voltage = voltage_level
        self.enable_source()
    except:
        return "An error has occurred.\nPossible reason: method must take a Keithley2400 object"
'''
'''
sourcemeter = Keithley2400("GPIB0::24::INSTR")

sourcemeter.measure_current()
print(sourcemeter.current)
sourcemeter.shutdown()
'''