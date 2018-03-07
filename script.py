import numpy as np
import simplekml
from polycircles import polycircles as pc
import math
import time
import pandas as pd
pd.set_option("display.max_rows",999)
pd.set_option('display.width', 1000)
from datetime import datetime, timedelta
from scipy.spatial import distance

#Var


#Constants
posGES = np.array([-2368.8, 4881.1, -3342.0])
posAES = np.array([-1293.0, 6238.3, 303.5])
c = 299792458/1000#km/s 

def getData(Time = 3):
	x = []
	y = []
	z = []
	vx = []
	vy = []
	vz = []
	lat = []
	lon = []
	dateSat = []
	alt = []
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
			vx.append(line.split()[7])
			vy.append(line.split()[8])
			vz.append(line.split()[9])
			lat.append(line.split()[10])
			lon.append(line.split()[11])
			alt.append(line.split()[12])
	dateSatd = []
	xd = []
	yd = []
	zd = []
	vxd = []
	vyd = []
	vzd = []
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
				vxd.append(vx[j])
				vyd.append(vy[j])
				vzd.append(vz[j])
				latd.append(lat[j])
				lond.append(lon[j])
				altd.append(alt[j])
				del dateSat[:j] 
				del x[:j]
				del y[:j]
				del z[:j]
				del vx[:j]
				del vy[:j]
				del vz[:j]
				del lat[:j]
				del lon[:j]
				del alt[:j]
				break
	data["DateSat"] = pd.Series(dateSatd)
	data["x"] = pd.Series(xd)
	data["y"] = pd.Series(yd)
	data["z"] = pd.Series(zd)
	data["vx"] = pd.Series(vxd)
	data["vy"] = pd.Series(vyd)
	data["vz"] = pd.Series(vzd)
	data["Lat"] = pd.Series(latd)
	data["Lon"] = pd.Series(lond)
	data["Alt"] = pd.Series(altd)
	data = data[['Date', 'DateSat', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'Lat', 'Lon', 'Alt', 'ChType', 'BTO', 'BFO']]#rearrange columns
	data.x = data.x.astype(float)
	data.y = data.y.astype(float)
	data.z = data.z.astype(float)
	data.vx = data.vx.astype(float)
	data.vy = data.vy.astype(float)
	data.vz = data.vz.astype(float)
	data.Lon = data.Lon.astype(float)
	data.Lat = data.Lat.astype(float)
	data.Alt = data.Alt.astype(float)
	data.BTO = data.BTO.astype(float)
	data.BFO = data.BFO.astype(float)
	return data

def inputR(inputText, wantedTextList):
	inp = False
	while inp == False:
		string = raw_input(inputText)
		if string in wantedTextList:inp = True
	return string 

def getBias(posSat):
	distSatGES = np.linalg.norm(posSat-posGES, axis = 1)
	distSatAES = np.linalg.norm(posSat-posAES, axis = 1)
	biasR = []
	biasT = []
	for i in range(len(data)):
		if data['ChType'][i]=="R-Channel RX":
			biasR.append((data['BTO'][i]*1e-6) - 2*(distSatAES[i]+distSatGES[i])/c )
		if data['ChType'][i]=="T-Channel RX":
			biasT.append((data['BTO'][i]*1e-6) - 2*(distSatAES[i]+distSatGES[i])/c )
	bias = []
	biasRn = 0
	biasTn = 0
	for i in range(len(data)):
		if data["Date"][i]==datetime(2014,3,7,16,41,52,907000):#TakeOff
			meanBiasR = np.mean(biasR)
			meanBiasT = np.mean(biasT)
			#meanBiasR = np.mean(np.append(biasR, biasT))
		if data["Date"][i]<=datetime(2014,3,7,16,29,52,406000):#preTakeOff
			if data['ChType'][i]=="R-Channel RX":
				bias.append(biasR[biasRn])
				biasRn = biasRn+1
			elif data['ChType'][i]=="T-Channel RX":
				bias.append(biasT[biasTn])
				biasTn = biasTn+1
		else:#postTakeOff	
			if data['ChType'][i]=="R-Channel RX": bias.append(meanBiasR)
			elif data['ChType'][i]=="T-Channel RX": bias.append(meanBiasT)
	bias = pd.Series(bias)
	return bias, distSatGES

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
	arcDates = getArcDates()
	data["BTO"][arcDates[0]] = data.iloc[arcDates[0]].loc["BTO"]-4600
	data["BTO"][arcDates[6]] = data.iloc[arcDates[6]].loc["BTO"]-4600
	data.to_csv("Data.csv")
if inString =="no":
	data = pd.read_csv("Data.csv")
	data = data.drop(['Unnamed: 0'], axis=1)
	data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S.%f')
	data['DateSat'] = pd.to_datetime(data['DateSat'], format='%Y-%m-%d %H:%M:%S.%f')
	arcDates = getArcDates()

#Some more data assignment
data["bias"], distSatGES = getBias(data.as_matrix(['x','y','z']))
data["Dist"] = (0.5*c*((data["BTO"].values*1e-6)-data["bias"].values)) - distSatGES 
pd.options.mode.chained_assignment = None
deltaSatAFC = np.zeros(len(data))
deltaFBias = np.full(len(data), 152.5)
data["deltaSatAFC"] = pd.Series(np.asarray(deltaSatAFC))
data["deltaFBias"] = pd.Series(np.asarray(deltaFBias))
data.deltaSatAFC = data.deltaSatAFC.astype(float)
data.deltaFBias = data.deltaFBias.astype(float)
data["deltaSatAFC"][arcDates[0]] = 10.8
data["deltaSatAFC"][arcDates[1]] = -1.2
data["deltaSatAFC"][arcDates[2]] = -1.3
data["deltaSatAFC"][arcDates[3]] = -17.9
data["deltaSatAFC"][arcDates[4]] = -28.5
data["deltaSatAFC"][arcDates[5]] = -37.7
data["deltaSatAFC"][arcDates[6]] = -38.0
data = data[data.deltaSatAFC != 0]
data = data.reset_index(drop=True)

#BTO Analysis
kml = simplekml.Kml()
sat = kml.newpoint(name='Satelite position at arbitary altitude')
sat.coords = [(np.mean(data["Lon"].values), np.mean(data["Lat"].values),357860)]
sat.altitudemode = 'relativeToGround'
arcIndexes = arcDates
arcNo = 0
for i in range(len(data)):
	arcNo = arcNo+1
	a = data["Dist"][i]
	b = np.square(data["x"][i])+np.square(data["y"][i])+np.square(data["z"][i])
	b = np.sqrt(b)
	c = 6371
	pheta = np.square(b)+np.square(c)-np.square(a)
	pheta = pheta / (2*b*c)
	pheta = np.arccos(pheta)
	radius = pheta*c
	datetime(2014,3,7,16,29,52,406000)
	radius = radius*1000
	print(str(radius/1000)+"km")
	if not np.isnan(radius):
		circle = pc.Polycircle(latitude=data["Lat"][i], longitude=data["Lon"][i], radius=radius, number_of_vertices=800)
		pol = kml.newpolygon(name="Arc"+str(arcNo), outerboundaryis=circle.to_kml())
		pol.style.polystyle.color = '000000ff'  # Transparent 
		pol.altitudemode = 'clampToGround'
		pol.tessellate = 1 
kml.save("Flight.kml")

#BFO Analysis
deltaFDown = []
for i in range(len(data)):
	v = np.array([data["vx"][i], data["vy"][i], data["vz"][i]], dtype=float)
	s = np.array([data["x"][i], data["y"][i], data["z"][i]], dtype=float)
	s = s-posGES
	vS = np.dot(v, s)/np.linalg.norm(s)
	FDown = 3615.1525e6
	deltaFDown.append(FDown*((c/(c+vS))-1))
data["deltaFDown"] = pd.Series(deltaFDown)
data.deltaFDown = data.deltaFDown.astype(float)
print(data)
data.to_csv("FinalData.csv")
