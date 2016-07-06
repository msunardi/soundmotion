import csv

def read(csv_path):
# Read KHR-1 .csv motion files, and return a formatted/filtered list of int
 

# setting up list variables
    l = []
    ll = []

# read .csv file and populate list
    for line in csv.reader(open(csv_path).readlines()[1:]):
        l.append(line)

# the data is a 2-dimensional list
# 'copy' the list and filter by removing the first three elements of each row element
    for i in range(len(l)):
        ll.append(l[i][3:])

# convert each element of the (filtered) list from string to integer
    for j in range(len(ll)):
        for k in range(len(ll[0])):
            ll[j][k] = int(ll[j][k])

	    # Filter the data (see /Documents/thesis-stuff/KHR-1-motions/servo_adjustments
	    if k in [2,5,8,12,15,16,18,21,22]:
		ll_ = lambda x: x + 90
	    elif k in [6,7]:
		ll_ = lambda x: x + 180
	    elif k in [13]:
		#ll_ = lambda x: abs(x-51)
		ll_ = lambda x: -x+51
	    elif k in [14]:
		ll_ = lambda x: x + 125
	    elif k in [19]:
		#ll_ = lambda x: abs(x-129)
		ll_ = lambda x: -x+129
	    elif k in [20]:
		ll_ = lambda x: x + 55
	    else:
		ll_ = lambda x: x
	    ll[j][k] = ll_(ll[j][k])

# show the new element (no quotes)
#    print ll

# use zip(*<list-name>) to transpose list of list or tuples
#    print zip(*ll)[0]

    newll = []
    ll = zip(*ll)

    for m in ll:
	m = list(m)
	newll.append(m)

#     return zip(*ll)
    return newll 
