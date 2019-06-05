import visa
import pymeasure

rm = visa.ResourceManager()
print(rm.list_resources('?*'))

from pymeasure.instruments.keithley import Keithley2400

sourcemeter = Keithley2400("GPIB::24")
sourcemeter.apply_current()
sourcemeter.source_current_range = 10e-3
sourcemeter.compliance_voltage = 10
sourcemeter.source_current = 0
sourcemeter.enable_source()

sourcemeter.measure_voltage()

sourcemeter.ramp_to_current(5e-3)
print(sourcemeter.voltage)

sourcemeter.shutdown()