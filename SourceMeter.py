import visa
import pymeasure

rm = visa.ResourceManager()
print(rm.list_resources('?*'))




from pymeasure.instruments.keithley import Keithley2400




sourcemeter = Keithley2400("GPIB0::24::INSTR")


sourcemeter.measure_current()

print(sourcemeter.current)


sourcemeter.shutdown()

