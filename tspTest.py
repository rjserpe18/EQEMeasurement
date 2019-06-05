import visa
import time
rm=visa.ResourceManager()



keithley = rm.open_resource('GPIB0::24::INSTR')


keithley.write('TRAC:FEED SENS')


keithley.write('TRAC:FEED SENS')