import visa
import pymeasure
from pymeasure.instruments.keithley import Keithley2400
import SourceMeter as SM

rm = visa.ResourceManager()
print(rm.list_resources())
keithley = Keithley2400("GPIB::24")
'''
print(get_current(keithley))

keithley.shutdown()
print(get_voltage(keithley))
keithley.shutdown()
print(get_resistance(keithley))
keithley.shutdown()
'''
SM.get_current(2)
SM.set_output_voltage(keithley, 5)
SM.set_output_current(keithley, 10e-3)
SM.zero_sources(keithley)