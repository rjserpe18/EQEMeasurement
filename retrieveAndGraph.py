from graphing_interface import interface
from csv import DictReader
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import visa

import plotly.plotly as py
import plotly.graph_objs as go

from pymeasure.instruments.keithley import Keithley2400
import time
import statistics
import SourceMeter as SM
from PowerMeter import PowerMeter
from graphing_interface import interface
from MonoChromater import MonoChromater


wavelengths = []
correctedEQE = []

numWavelengths = []
numEQEVals = []

eQEVals = []
colors=(0,0,0)
area = np.pi*3

with open("EQE_Data_6_17_new_2.csv") as f:
    eQEVals = [row["EQE - Uncorrected"] for row in DictReader(f)]

    for val in eQEVals:

        numEQEVals.append(float(val)*-1)

with open("EQE_Data_6_17_new_2.csv") as f:
    wavelengths = [row["Wavelength"] for row in DictReader(f)]

    for val in wavelengths:

        numWavelengths.append(float(val))




print(numWavelengths)
print(numEQEVals)

print(numWavelengths.__len__())
print(numEQEVals.__len__())

interface([[numWavelengths,numEQEVals]])




# power at powerMeter position  ----  0.0002000981768
# power at DUT position ---- 0.0001671820064

# correction factor 1.1969

