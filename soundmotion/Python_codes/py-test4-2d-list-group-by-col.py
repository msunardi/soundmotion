import csv

# setting up list variables
l = []
ll = []

# read .csv file and populate list
#for line in csv.reader(open("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv").readlines()[1:]):
for line in csv.reader(open("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv").readlines()[1:]):
   l.append(line)

# the data is a 2-dimensional list
# 'copy' the list and filter by removing the first three elements of each row element
for i in range(len(l)):
#    print l[i][3:]
    ll.append(list(l[i][3:]))

# convert each element of the (filtered) list from string to integer
for j in range(len(ll)):
    for k in range(len(ll[0])):
        ll[j][k] = int(ll[j][k])

# show the new element (no quotes)
#print ll

for gb in ll:
    print gb[:12]

# use zip(*<list-name>) to transpose list of list or tuples
a = []
a = zip(*ll)
#print zip(*ll)
print a[0]
print zip(*a)[0]

b = []
for ea in a:
    ea = list(ea)
    b.append(ea)
print b
