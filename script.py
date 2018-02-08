import numpy as np
from datetime import datetime
from scipy.spatial import distance

#Initialisation
date = []
x = []
y = []
z = []
vx = []
vy = []
vz = []
lat = []
lon = []
 
#Constants
posGES = np.array((-2368.8, 4881.1, -3342.0))
posAES = np.array((-1293.0, 6238.3, -303.5))

Report = open("Report", "r")
lines = Report.readlines()
print("First two lines: \n")
for i, line in enumerate(lines):
	if i <=1:
		print(line, "\n\n")
	if "Nov" in line:
		print(line)
		lines.pop(i) 
		#May not be working not sure if git took out rest of file?
		#print(lines[17868])
	if i!=0:
		date.append(line.split("  ")[0])
		x.append(line.split()[4])
		y.append(line.split()[5])
		z.append(line.split()[6])
		vx.append(line.split()[7])
		vy.append(line.split()[8])
		vz.append(line.split()[9])
		lat.append(line.split()[10])
		lon.append(line.split()[11])
#print(x[0], y[0], z[0], vx[0], vy[0], vz[0], lat[0], lon[0])

for i in range(len(date)):
	date[i] = datetime.strptime(date[i], "%d %b %Y %H:%M:%S.%f") 
posSat = np.column_stack((np.asarray(x, dtype=float),np.asarray(y, dtype=float),np.asarray(z, dtype=float)))
velSat = np.column_stack((np.asarray(vx, dtype=float),np.asarray(vy, dtype=float),np.asarray(vz, dtype=float)))

distSatGES = np.linalg.norm(posSat-posGES, axis=1)
distSatAES = np.linalg.norm(posSat-posAES, axis=1)
print(distSatGES)
print(distSatAES)

