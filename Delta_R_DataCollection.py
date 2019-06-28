from graphing_interface import interface
import csv
from os import listdir
from os.path import isfile

files = [f for f in listdir('.') if isfile(f)]
full_data = []

for filename in files:
    if filename.endswith(".txt"):
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            data = []
            for row in readCSV:

                data.append(row)
            data = data[2:]
            dataset = []
            gdata = []
            current = []
            voltage = []
            for row in data:
                try:
                    row = row[0]
                    row = row.split('\t')
                    cur_val = row[1]
                    vol_val = row[0]
                    cur_val = float(cur_val) *10**9
                    vol_val = float(vol_val)
                    current.append(cur_val)
                    voltage.append((vol_val))
                except:
                    pass
                dataset.append(row)
            gdata.append(voltage)
            gdata.append(current)
            full_data.append(gdata)
print(full_data)
interface(full_data)