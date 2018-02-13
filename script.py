import numpy as np
import math
import time
import pandas as pd
from datetime import datetime, timedelta
from scipy.spatial import distance

#Constants
posGES = np.array([-2368.8, 4881.1, -3342.0])
posAES = np.array([-1293.0, 6238.3, 303.5])

def getData():
z = []
vx = []
vy = []
vz = []
lat = []
lon = []
dateSat = []
x = []
y = []
	#begin
	#Grab InmarSat Data
	data = pd.read_csv("inmarsat.csv", usecols=[0,8,25,27])
	data.rename(columns={'Time':'Date', 'Frequency Offset (Hz)': 'BFO', 'Burst Timing Offset (microseconds)': 'BTO', 'Channel Type': 'ChType'}, inplace=True)
	data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y %H:%M:%S.%f')

	#Grab report data
	Report = open("Report", "r")
	lines = Report.readlines()

	#Grab report data
	for i, line in enumerate(lines):
		#if i <=1:
		#       print(line, "\n\n")
		if "Nov" in line:
			print(line)
			lines.pop(i)
			#May not be working not sure if git took out rest of file?
			#print(lines[17868])
		if i!=0:
			dateSat.append(datetime.strptime(line.split("  ")[0], "%d %b %Y %H:%M:%S.%f"))
			x.append(line.split()[4])
			y.append(line.split()[5])
			z.append(line.split()[6])
			#vx.append(line.split()[7])
			#vy.append(line.split()[8])
			#vz.append(line.split()[9])
			#lat.append(line.split()[10])
			#lon.append(line.split()[11])
	dataSat = []
	xd = []
	yd = []
	zd = []
	data = data[pd.notnull(data['BTO'])]
	data = data.reset_index(drop=True)
	data = data[pd.notnull(data['BTO'])]
	data = data.reset_index(drop=True)
	for i in range(len(data)):
		print(data['Date'][i])
		if data['Date'][i]==datetime(2014,3,7,16,41,52,907000):break#stop at 4:30 for speed
		#if data['Date'][i]==datetime(2014,3,7,16,6,34,906000):break#stop at 4:06 for speed
		for j in range(len(dateSat)):
			if abs(dateSat[j]-data['Date'][i])<=timedelta(0,0,0,50):
				dataSat.append(dateSat[j])
				xd.append(x[j])
				yd.append(y[j])
				zd.append(z[j])
				break
	data["DateSat"] = pd.Series(dataSat)
	data["x"] = pd.Series(xd)
	data["y"] = pd.Series(yd)
	data["z"] = pd.Series(zd)
	data = data[['Date', 'DateSat', 'x', 'y', 'z', 'ChType', 'BFO', 'BTO']]#rearrange columns
	data.x = data.x.astype(float)
	data.y = data.y.astype(float)
	data.z = data.z.astype(float)
	data.BTO = data.BTO.astype(float)
	data.BFO = data.BFO.astype(float)
	return data


#BTO
posSat = data.as_matrix(['x', 'y', 'z'])#Take xyz data out of data frame
posSat = posSat[~np.isnan(posSat).any(axis=1)]#Take NaNs out of data
distSatGES = np.linalg.norm(posSat-posGES, axis = 1)
distSatAES = np.linalg.norm(posSat-posAES, axis = 1)
c = 3e5
for i in range(len(data)):
	if data['ChType'][i]=="R-Channel RX":
		biasR = (2*(distSatAES+distSatGES))/c + (data['BTO'][i]*1e-6)
	if data['ChType'][i]=="T-Channel RX":
		biasT = (2*(distSatAES+distSatGES))/c + (data['BTO'][i]*1e-6)
print(np.mean(biasR))
print(np.mean(biasT))

