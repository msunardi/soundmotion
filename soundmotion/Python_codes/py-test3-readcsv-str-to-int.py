import csv

# setting up list variables
l = []
ll = []

# read .csv file and populate list
for line in csv.reader(open("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv").readlines()[1:]):
    l.append(line)

# the data is a 2-dimensional list
# 'copy' the list and filter by removing the first three elements of each row element
for i in range(len(l)):
    print l[i][3:]
    ll.append(l[i][3:])

# show the length of each row of the new (filtered) list
print len(ll[0])

# show the new list
print ll               

# convert each element of the (filtered) list from string to integer
for j in range(len(ll)):
    for k in range(len(ll[0])):
        ll[j][k] = int(ll[j][k])

# show the new element (no quotes)
print ll

# test if the elements are now really integers
print ll[0][0]+1
