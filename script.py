import numpy as np
import time
from datetime import datetime, timedelta
from scipy.spatial import distance

#Initialisation
dateSat = []
date = []
x = []
y = []
z = []
vx = []
vy = []
vz = []
lat = []
lon = []
dates = []
datesSat = []
#not sure if length of data obtained from csv is correct +-1
 
#Constants
posGES = np.array((-2368.8, 4881.1, -3342.0))
posAES = np.array((-1293.0, 6238.3, -303.5))

#begin
#Grab ImarSat Data
data = np.genfromtxt(fname='inmarsat.csv', delimiter=',', dtype=str, skip_header=1)

#Convert Imarsate dates into array in datetime format
#example date: 7/03/2014 16:00:13.406
for i in range(len(data)):
	date.append(datetime.strptime(data[i][0], "%d/%m/%Y %H:%M:%S.%f")) 

Report = open("Report", "r")
lines = Report.readlines()
print("First two lines: \n")

#Grab report data
for i, line in enumerate(lines):
	if i <=1:
		print(line, "\n\n")
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

#Put xyz into pos numpy array
posSat = np.column_stack((np.asarray(x, dtype=float),np.asarray(y, dtype=float),np.asarray(z, dtype=float)))
velSat = np.column_stack((np.asarray(vx, dtype=float),np.asarray(vy, dtype=float),np.asarray(vz, dtype=float)))

#Calculate eucluedian distances
#distSatGES = np.linalg.norm(posSat-posGES, axis=1)
#distSatAES = np.linalg.norm(posSat-posAES, axis=1)

print(data[1][25])

for i in range(len(date)):
	if date[i]==datetime(2014,3,7,16,41,52,907000):
		break
	if data[i][25]!='':
		for j in range(len(dateSat)):
			if (((dateSat[j]-date[i])<=timedelta(0,0,0,100)) and (dateSat[j]>date[i])) or (((dateSat[j]-date[i])>=timedelta(0,0,0,100)) and (dateSat[j]<date[i])):
				print(date[i])
				dates.append(date[i])		
				datesSat.append(dateSat[j])
for i in range(len(dates)):
	print(dates[i], datesSat[i])
#Still rounding up
