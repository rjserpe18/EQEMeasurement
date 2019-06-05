import visa
import pymeasure
from pymeasure.instruments.keithley import Keithley2400
from SourceMeter import get_current

rm = visa.ResourceManager()
print(rm.list_resources())
keithley = Keithley2400("GPIB::24")

#keithley.write(":CONFigure:RESIstance")

#keithley.enable_source()
#keithley.measure_voltage() 
'''
keithley.source_current_range = 10e-3 # Sets the source current range to 10 mA
keithley.compliance_voltage = 10 # Sets the compliance voltage to 10 V
keithley.source_current = 0 # Sets the source current to 0 mA
keithley.enable_source() # Enables the source output
keithley.measure_voltage() # Sets up to measure voltage
keithley.ramp_to_current(5e-3) # Ramps the current to 5 mA
print(keithley.voltage) # Prints the voltage in Volts
keithley.shutdown()
'''
print(get_current(keithley))
keithley.shutdown()