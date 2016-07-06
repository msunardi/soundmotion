""" =====================================
    Load from KHR-1 .csv motion files, and interpolate each segment/point/frame
    Parameters:
	a KHR-1 .csv motion file

    Returns:
	an interpolated list of motion for one KHR-1 channel/servo (#1)
    ====================================
"""

import csv
import interpolation

# setting up list variables
l = []
ll = []

# read .csv file and populate list
for line in csv.reader(open("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv").readlines()[1:]):
    l.append(line)

# the data is a 2-dimensional list
# 'copy' the list and filter by removing the first three elements of each row element
for i in range(len(l)):
#    print l[i][3:]
    ll.append(l[i][3:])

# convert each element of the (filtered) list from string to integer
for j in range(len(ll)):
    for k in range(len(ll[0])):
        ll[j][k] = int(ll[j][k])

# show the new element (no quotes)
#print ll

# use zip(*<list-name>) to transpose list of list or tuples
ll_zip = []
ll_zip = zip(*ll)
print ll_zip[0]

interpolate = interpolation.hermiteInterpolate

print ll_zip[0][0], ll_zip[0][1], ll_zip[0][2], ll_zip[0][3]
print interpolate(ll_zip[0][0], ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], 0),
print interpolate(ll_zip[0][0], ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], 0.25),
print interpolate(ll_zip[0][0], ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], 0.5),
print interpolate(ll_zip[0][0], ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], 0.75),
print interpolate(ll_zip[0][0], ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], 1)
print interpolate(ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], ll_zip[0][4], 0),
print interpolate(ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], ll_zip[0][4], 0.25),
print interpolate(ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], ll_zip[0][4], 0.5),
print interpolate(ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], ll_zip[0][4], 0.75),
print interpolate(ll_zip[0][1], ll_zip[0][2], ll_zip[0][3], ll_zip[0][4], 1)

m = []
m_temp = []
#for point in ll_zip:
point = ll_zip[0]

#for index in range(len(point)):
#    print index
#    while index < len(point)-3:
for index in range(len(point)-3):
#    print index
    for mu in [0, 0.125,  0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
        p = interpolate(point[index], point[index+1], point[index+2], point[index+3], mu, 0, 0)
        m_temp.append(p)
    m.extend(m_temp)
    m_temp = []

    if index == len(point)-4:
        for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
            p = interpolate(point[index+1], point[index+2], point[index+3], point[index+3], mu, 0, 0)
            m_temp.append(p)
        p = interpolate(point[index+1], point[index+2], point[index+3], point[index+3], 1, 0, 0)
        m_temp.append(p)
        m.extend(m_temp)
        m_temp = []

"""
 p = interpolate(point[index+1], point[index+2], point[index+3], point[index+3], 1, 0, 0)
        m.append(p)
"""
print m      
