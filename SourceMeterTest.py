import visa
import pymeasure
from pymeasure.instruments.keithley import Keithley2400
import SourceMeter as SM



rm = visa.ResourceManager()
print(rm.list_resources())
keithley = Keithley2400("GPIB1::1::INSTR")
print(SM.get_current(keithley))
keithley.shutdown()
