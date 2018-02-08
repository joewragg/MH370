import numpy as np
Report = open("Report", "r")
lines = Report.readlines()
#print(type(lines[1]))
for i, line in enumerate(lines):
    if "2029" in line:
        print(i)
        lines.pop(i) 
print(lines[1430])
print(lines[17868])
#data = np.loadtxt("Report",skiprows=1,usecols=(0,1,2))
#print(lines)
#print(data[0])
testF = open("testF", "w")
#write(result)
testF.close()
