from graphing_interface import interface
from csv import DictReader
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

import plotly
import plotly.graph_objs as go
from pymeasure.instruments.keithley import Keithley2400
import time
import statistics
import SourceMeter as SM
from PowerMeter import PowerMeter
from graphing_interface import interface




wavelengths = []
correctedEQE = []
eQEVals = []
colors=(0,0,0)
area = np.pi*3


with open("EQE_Data_6_17_new.csv") as f:
    eQEVals = [row["EQE"] for row in DictReader(f)]

    for val in eQEVals:
        val = float(val)*-1
        correctedEQE.append(val)


with open("EQE_Data_6_17_new.csv") as f:
    wavelengths = [row["wavlength"] for row in DictReader(f)]


# Create a trace
trace = go.Scatter(
    x = wavelengths,
    y = correctedEQE,
    mode = 'markers'
)


interface(wavelengths, eQEVals)

#
#
# data = [trace]
#
# plotly.offline.plot(data)
#


#power at powerMeter position  ----  0.0002000981768
#power at DUT position ---- 0.0001671820064

#correction factor 1.1969


