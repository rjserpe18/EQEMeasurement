import visa
import time

rm=visa.ResourceManager()



keithley = rm.open_resource('GPIB0::24::INSTR')























keithley.write('*RST')

keithley.write(':SOUR:FUNC VOLT')
keithley.write(':SOUR:VOLT:MODE SWEEP')
keithley.write(':SOUR:DEL 0')

keithley.write(':SOUR:SWE:SPAC LIN')


keithley.write(':SENSe:CURR:PROT 10e-3')

keithley.write(':SOUR:VOLT:START 0')

keithley.write(':SOUR:VOLT:STOP 5')

keithley.write(':TRAC:POIN 101')

keithley.write(':TRIG:COUN 101')

keithley.write(':SOUR:VOLT:STEP 0.05')

keithley.write(':TRAC:FEED SENS')

keithley.write(':TRAC:FEED:CONT NEXT')

keithley.write(':OUTPut ON')




'''
'''
