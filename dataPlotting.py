import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import pandas as pd

import csv

columns = []
word_list = []


asTextFile = open('EQE_Data.csv','r')
columns = asTextFile.read().split('\n')

i = 0

# clearing the file

filename = 'EQE_Data_Formatted.csv'
f = open(filename,"w+")
f.close()

wavelengths = []
eQEVals = []

with open('EQE_Data_Formatted.csv', 'a') as csvFile:
    cwriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)


    cwriter.writerow(['wavlength','power (mW)','current (uA)','EQE'])


    for row in columns:

        values = columns[i].split(',')

        wavelength= values[0]
        formattedPower = round(1000*float(values[1]),3)
        formattedCurrent = round(1000000*float(values[2]),11)

        wavelengths.append(values[0])



        if (formattedCurrent == 0):
            currentByPower = 0
        else:
            currentByPower = formattedCurrent/(formattedPower*1000)

        eQE = 100 * (10**(9) * 1.24*10**(-6) * currentByPower) / float(wavelength)

        eQE = round(eQE,1)

        eQEVals.append((eQE))

        currentRow = [values[0], formattedPower , formattedCurrent, (eQE)]

        cwriter.writerow(currentRow)

        i+=1

