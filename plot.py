import matplotlib.pyplot as plt
import numpy as np
import csv

lists = []
with open("pos.csv", 'r') as cfile:
    # lines = cfile.readlines()
    # lines_aux = [line.split() for line in lines if line.strip()]
    reader = csv.reader(cfile)
    for row in reader:
        text = row[0]
        values = text.split()
        lists.append(float(values[2]))
        # print(values[2])

array = np.array(lists)

plt.hist(array, bins=100)

plt.show()
