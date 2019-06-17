import visa
import time
from PowerMeter import PowerMeter

rm = visa.ResourceManager()
print(rm.list_resources())
