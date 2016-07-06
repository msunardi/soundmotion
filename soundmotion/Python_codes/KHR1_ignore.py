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

""" Load the interpolation function (format: hermiteInterpolate(y0, y1, y2, y3, mu, bias, tension)
y0, y1, y2, y3 = points (angles) to interpolate (hermite requires 4 points, or 3 segments (a segment consists of 2 points))
y1, y2 = interpolation is between these two points
y0 = point before y1
y3 = point after y2
mu = interpolation position [0,1] (0 gives: y1, 1 gives: y2)
bias = bias parameter (0 = neutral (default), -1 = towards first segment, +1 = towards second segment)
tension = tension parameter [0,1] (0 = neutral (default), -1 = low, +1 = high)
"""

interpolate = interpolation.hermiteInterpolate

# Create a 'channel list' (channel = list of positions of one servo)
m = []

# Create a temporary list for the interpolation points
m_temp = []

# A new list for the whole motion
m_all = []

for point in ll_zip:
# For each list element -- in this case, a KHR-1 'channel'...

    for index in range(len(point)-3):
# ...for each position of the channel...	

        for mu in [0, 0.125,  0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
# ...interpolate 2 points by adding 7 equally separated (distance: 1/2^3) points in between...
            p = interpolate(point[index], point[index+1], point[index+2], point[index+3], mu, 0, 0)
            m_temp.append(p)

# Add the interpolation points to the 'channel list'
        m.extend(m_temp)
        m_temp = []

        if index == len(point)-4:
# If reaching the end of the list, do one last interpolation for the last segment (connecting the last point)

            for mu in [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]:
                p = interpolate(point[index+1], point[index+2], point[index+3], point[index+3], mu, 0, 0)
                m_temp.append(p)

            p = interpolate(point[index+1], point[index+2], point[index+3], point[index+3], 1, 0, 0)
            m_temp.append(p)
            m.extend(m_temp)
            m_temp = []

# Add the interpolated channel to the new motion list
    m_all.append(m)

# Clear the 'channel list' to be used for the next channel
    m = []

print m_all
