import numpy as np
import simplekml
from polycircles import polycircles as pc
import math
import time
import pandas as pd
pd.set_option("display.max_rows",999)
pd.set_option('display.width', 1000)
from datetime import datetime, timedelta
import geopy
from geopy.distance import VincentyDistance
from scipy.spatial import distance
from sympy.solvers import solve
from sympy import Symbol

#Var


#Constants
posGES = np.array([-2368.8, 4881.1, -3342.0])
posAES = np.array([-1293.0, 6238.3, 303.5])
c = 299792458/1000#km/s 
iterationConstant = 8000
alt = 10668*1e-3

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
			meanBiasT = -0.495679
			meanBiasR=meanBiasT
			print(meanBiasR)
			print(meanBiasT)
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
				arcIndexes.append(j)	
	return arcIndexes

def lla_to_ecef(lat, lon, alt):
    import pyproj
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    x, y, z = pyproj.transform(lla, ecef, lon, lat, alt, radians=False)
    return x, y, z

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

def drawPoint(Name, Lat, Lon, Alt):
	pnt = kml.newpoint(name= Name)
	pnt.coords = [(Lon, Lat, Alt)]
	pnt.altitudemode = 'relativeToGround'
	return 1

def drawCircle(Name, Lat, Lon, Radius, color):
	circle = pc.Polycircle(latitude=Lat, longitude=Lon, radius=Radius, number_of_vertices=iterationConstant)
	pol = kml.newpolygon(name=Name, outerboundaryis=circle.to_kml())
	pol.style.polystyle.color ="000000ff"   # Transparent 
	pol.style.linestyle.color = color
	pol.altitudemode = 'absoluteAltitude'
	pol.tessellate = 1 
	return circle

def drawLine(Name, originLat, originLon, destLat, destLon, color):
	ls = kml.newlinestring(name = Name)
	ls.style.linestyle.color = color
	ls.coords = [(originLon, originLat), (destLon, destLat)]
	return 1

#BTO Analysis
kml = simplekml.Kml()
drawPoint("Satposition", np.mean(data["Lon"].values), np.mean(data["Lat"].values),357860)
arcIndexes = arcDates
arcNo = 0

circles = []
for i in range(len(data)):
	arcNo = arcNo+1
	a = data["Dist"][i]
	b = np.square(data["x"][i])+np.square(data["y"][i])+np.square(data["z"][i])
	b = np.sqrt(b)
	c = 6371+alt#+73
	#c = 6371+alt+50
	pheta = np.square(b)+np.square(c)-np.square(a)
	pheta = pheta / (2*b*c)
	pheta = np.arccos(pheta)
	radius = c*pheta
	datetime(2014,3,7,16,29,52,406000)
	radius = radius*1000
	circles.append(drawCircle("Arc"+str(arcNo), data["Lat"][i], data["Lon"][i], radius, simplekml.Color.white))
	print(str(radius/1000)+"km")

def getFComp(posPl, speed, posSat):
	v = v/1000
	#sat = [0,64.5,35786*1e3]
	#sat = lla_to_ecef(sat[0], sat[1], sat[2])
	#sat = np.array(sat)*1e-3
	s = posSat-posPl
	vs = np.dot(v,s)
	vs = vs/np.linalg.norm(s)
	Fup = 1646.6525*1e6
	deltaFComp = Fup*(((c+vs)/c)-1)
	return deltaFComp

def findShortest(name, radius, origin, alt, circle, direction):
	distArr = []
	circle = circle.to_lat_lon()
	lastDist = 99999
	for i in range(len(circle)):
		destination = geopy.Point(circle[i][0], circle[i][1], alt)
		distance = VincentyDistance(origin, destination).meters	
		dist = distance-radius
		if (lastDist>0) and (dist<0) and (direction=="North"):
			minDist = dist
			j = i
		if (lastDist<0) and (dist>0) and (direction=="South"):
			minDist = dist
			j = i
		lastDist = dist
	return geopy.Point(circle[j][0], circle[j][1], alt)

def drawPath(origin, dest, time, no):
	if time.minute<10:
		drawPoint(str(time.hour)+":0"+str(time.minute), dest.latitude, dest.longitude, alt)
	else:
		drawPoint(str(time.hour)+":"+str(time.minute), dest.latitude, dest.longitude, alt)
	drawLine("Path"+str(no), origin.latitude, origin.longitude, dest.latitude, dest.longitude, simplekml.Color.red)
	return 1 

def getDest(origin, lastTime, time, bearing):
	deltaT = abs(lastTime-time).total_seconds()
	radius = speed*deltaT
	dest = VincentyDistance(kilometers=radius*1e-3).destination(origin, bearing)
	return dest

alt = alt*1000
speed = 243.322#cruising Speed
time = datetime(2014,3,7,17,6,43)
origin = geopy.Point(2.7, 101.7, 0)
dest = geopy.Point(5.27, 102.79, alt)
drawPath(origin, dest, time, 1) 

origin = dest
lastTime = time
time = datetime(2014, 3, 7, 17, 21, 13)
dest = getDest(origin, lastTime, time, 25)
drawPath(origin, dest, time, 2)

origin = dest
lastTime = time
time = datetime(2014,3,7,17,52,27)
dest = geopy.Point(5.2, 100.2, alt)
drawPath(origin, dest, time, 3)

origin = dest
lastTime = time
time = datetime(2014,3,7,18,22,12)
dest = geopy.Point(6.65, 96.34, alt)
drawPath(origin, dest, time, 4)

speed = 320#Max speed
origin = dest
lastTime = time
time = data["Date"][0]
deltaT = abs(lastTime-time).total_seconds()
radius = speed*deltaT
print(data)
destArr = []
dest = findShortest("test", radius, origin, alt, circles[0], "North")	
destArr.append(dest)
firstArcPos = dest
drawPath(origin, dest, time, 5)

speed = 243.322#cruising Speed
#speed = 257.322#500knots
for i in range(0,6):
	origin = dest
	deltaT = abs(data["Date"][i+1]-data["Date"][i]).total_seconds()
	radius = speed*deltaT
	print(data["Date"][i+1].hour)
	time = data["Date"][i+1]
	dest = findShortest("test", radius, origin, alt, circles[i+1], "South")
	destArr.append(dest)
	drawPath(origin, dest, time, 5+i)
print('\n')

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

maxAlt = 10668#35kfeet
glideDist = maxAlt*16.995
print(glideDist)
drawCircle("Glide", destArr[6].latitude, destArr[6].longitude, glideDist, simplekml.Color.white) 
drawPoint("Their location", -35.6, 92.8, 0)

kml.save("Flight.kml")
#Arc0
data.to_csv("FinalData.csv")
