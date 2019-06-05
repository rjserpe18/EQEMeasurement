import visa
import time

rm=visa.ResourceManager()



keithley = rm.open_resource('GPIB0::24::INSTR')



keithley.write("*RST")











#print(keithley.write(':MEASure[:<function>]?'))
