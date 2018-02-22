import numpy as np
import simplekml
from polycircles import polycircles as pc
import math
import time
import pandas as pd
from datetime import datetime, timedelta
from scipy.spatial import distance

#Var


#Constants
posGES = np.array([-2368.8, 4881.1, -3342.0])
posAES = np.array([-1293.0, 6238.3, 303.5])
c = 3e5

def getData(Time = 3):
	z = []
	vx = []
	vy = []
	vz = []
	lat = []
	lon = []
	dateSat = []
	x = []
	y = []
	alt = []
		#begin
	#Grab InmarSat Data
	data = pd.read_csv("inmarsat.csv", usecols=[0,8,25,27])
	data.rename(columns={'Time':'Date', 'Frequency Offset (Hz)': 'BFO', 'Burst Timing Offset (microseconds)': 'BTO', 'Channel Type': 'ChType'}, inplace=True)
	data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y %H:%M:%S.%f')
	#Grab report data
	Report = open("Report.txt", "r")
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
			lat.append(line.split()[10])
			lon.append(line.split()[11])
			alt.append(line.split()[12])
	dateSatd = []
	xd = []
	yd = []
	zd = []
	lond = []
	latd = []
	altd = []
	data = data[pd.notnull(data['BTO'])]
	data = data.reset_index(drop=True)
	data = data[pd.notnull(data['BTO'])]
	data = data.reset_index(drop=True)
	for i in range(len(data)):
		print(data['Date'][i])
		for j in range(len(dateSat)):
			if abs(dateSat[j]-data['Date'][i])<=timedelta(0,0,0,50):
				dateSatd.append(dateSat[j])
				xd.append(x[j])
				yd.append(y[j])
				zd.append(z[j])
				print(data["Date"][i], dateSat[j], z[j])
				latd.append(lat[j])
				lond.append(lon[j])
				altd.append(alt[j])
				del dateSat[:j] 
				del x[:j]
				del y[:j]
				del z[:j]
				del lat[:j]
				del lon[:j]
				del alt[:j]
				break
	data["DateSat"] = pd.Series(dateSatd)
	data["x"] = pd.Series(xd)
	data["y"] = pd.Series(yd)
	data["z"] = pd.Series(zd)
	data["Lat"] = pd.Series(latd)
	data["Lon"] = pd.Series(lond)
	data["Alt"] = pd.Series(altd)
	data = data[['Date', 'DateSat', 'x', 'y', 'z', 'Lat', 'Lon', 'Alt', 'ChType', 'BFO', 'BTO']]#rearrange columns
	data.x = data.x.astype(float)
	data.y = data.y.astype(float)
	data.z = data.z.astype(float)
	data.Lon = data.Lon.astype(float)
	data.Lat = data.Lat.astype(float)
	data.Alt = data.Alt.astype(float)
	data.BTO = data.BTO.astype(float)
	data.BFO = data.BFO.astype(float)
	print(data)
	return data

def inputR(inputText, wantedTextList):
	inp = False
	while inp == False:
		string = raw_input(inputText)
		if string in wantedTextList:inp = True
	return string 

def getDist(posSat):
	posSat = posSat[~np.isnan(posSat).any(axis=1)]#Take NaNs out of data
	distSatGES = np.linalg.norm(posSat-posGES, axis = 1)
	distSatAES = np.linalg.norm(posSat-posAES, axis = 1)
	return distSatGES, distSatAES

def getBias(posSat):
	distSatGES, distSatAES = getDist(posSat)
	for i in range(len(data)):
		if data['ChType'][i]=="R-Channel RX":
			biasR = (data['BTO'][i]*1e-6) - 2*(distSatAES+distSatGES)/c 
		if data['ChType'][i]=="T-Channel RX":
			biasT = (data['BTO'][i]*1e-6) - 2*(distSatAES+distSatGES)/c  #old = (2*(distSatAES+distSatGES))/c + (data['BTO'][i]*1e-6)
	biasR = np.mean(biasR)
	biasT = np.mean(biasT)
	bias = []
	meanBias = (biasR+biasT)/2
	for i in range(len(data)):
		if data['ChType'][i]=="R-Channel RX": bias.append(biasT)
		elif data['ChType'][i]=="T-Channel RX": bias.append(biasT)#test
		else: bias.append(biasR)
	bias = pd.Series(bias)
	return bias

def getDistSatPlane(posSat):
	distSatGES, distSatAES = getDist(posSat)
	distSatPlane = (0.5*c*((data["BTO"].values*1e-6)-data["bias"].values)) - distSatGES 
	return distSatPlane

def remChannelFromData(channel):
	dropList = []
	for i in range(len(data)):
		if data['ChType'][i]==channel:
			dropList.append(i)	
			print(data['ChType'][i])
	newData = data.drop(dropList)
	newData = newData.reset_index(drop=True)
	return newData

def getArcDates():
	arcDate = []
	arcIndexes = [] 
	arcDate.append(datetime(2014,3,7,18,25,27))
	arcDate.append(datetime(2014,3,7,19,41,00))
	arcDate.append(datetime(2014,3,7,20,41,00))
	arcDate.append(datetime(2014,3,7,21,41,24))
	arcDate.append(datetime(2014,3,7,22,41,19))
	arcDate.append(datetime(2014,3,8,0,10,58))
	arcDate.append(datetime(2014,3,8,0,19,29))
	for i in range(len(arcDate)):
		for j in range(len(data)):
			if abs(data["Date"][j]-arcDate[i])<=timedelta(0,5):
				print(data["Date"][j], arcDate[i])
				arcIndexes.append(j)	
	return arcIndexes

inString = inputR("Get data? yes/no: ", ["yes", "no"])
if inString =="yes":
	data = getData()
if inString =="no":
	data = pd.read_csv("FinalData.csv")
	data = data.drop(['Unnamed: 0'], axis=1)
	data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S.%f')
	data['DateSat'] = pd.to_datetime(data['DateSat'], format='%Y-%m-%d %H:%M:%S.%f')
data["bias"] = getBias(data.as_matrix(['x','y','z']))
data["Dist"] = getDistSatPlane(data.as_matrix(['x','y','z']))
data.bias = data.bias.astype(float)
#data = remChannelFromData("R-Channel RX")#########################################
print(data)
data.to_csv("FinalData.csv")

#Main
kml = simplekml.Kml()
sat = kml.newpoint(name='Satelite position at arbitary altitude')
sat.coords = [(np.mean(data["Lon"].values), np.mean(data["Lat"].values),357860)]
sat.altitudemode = 'relativeToGround'

arcIndexes = getArcDates()
arcNo = 0
for i in arcIndexes:
	arcNo = arcNo+1
	a = data["Dist"][i]
	b = data["y"][i]
	#b = data["Alt"][i]+6371
	c = 6371+10
	pheta = np.square(b)+np.square(c)-np.square(a)
	pheta = pheta / (2*b*c)
	pheta = np.arccos(pheta)
	radius = pheta*c
	a = 2*np.square(c)
	a = a - ((2*np.square(c))*np.cos(pheta))
	a = np.sqrt(a)
	radius = radius*1000
	print(str(radius/1000)+"km")
	if not np.isnan(radius):
		circle = pc.Polycircle(latitude=data["Lat"][i], longitude=data["Lon"][i], radius=radius, number_of_vertices=400)
		pol = kml.newpolygon(name="Arc"+str(arcNo), outerboundaryis=circle.to_kml())
		pol.style.polystyle.color = '000000ff'  # Transparent 
		pol.altitudemode = 'clampToGround'
		pol.tessellate = 1 
kml.save("Flight.kml")
