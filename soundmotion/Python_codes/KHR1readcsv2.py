import csv

source = "[KHR1readscv2]"

def read(csv_path):
# Read KHR-1 .csv motion files, and return a formatted/filtered list of int
	print "%s Path: %s" % (source, csv_path)

# setting up list variables
	l = []
	ll = []

# read .csv file and populate list
	try:
		for line in csv.reader(open(csv_path).readlines()[1:]):
			l.append(line)
		print "%s success!" % source
	except:
		print "%s Error!" % source

	# print "[KHR1readcsv2] Data: %s" % l

# the data is a 2-dimensional list
# 'copy' the list and filter by removing the first three elements of each row element
	for i in range(len(l)):
		ll.append(l[i][3:])

	# print "%s ll: %s" % (source, ll)

# convert each element of the (filtered) list from string to integer
	# for j in range(len(ll)-1):
	# 	for k in range(len(ll[0])-1):
	# 		#ll[j][k] = int(ll[j][k])
	# 		#print "lala", ll[j][k]
	# 		x = adjustData(k+1, int(ll[j][k]))
	# 		#print x
	# 		ll[j][k] = x
	# 		#print "lolo"

	# 		# Filter the data (see /Documents/thesis-stuff/KHR-1-motions/servo_adjustments
	# 		"""if k in [2,5,8,12,15,16,18,21,22]:
	# 		ll_ = lambda x: x + 90
	# 		elif k in [6,7]:
	# 		ll_ = lambda x: x + 180
	# 		elif k in [13]:
	# 		#ll_ = lambda x: abs(x-51)
	# 		ll_ = lambda x: -x+51
	# 		elif k in [14]:
	# 		ll_ = lambda x: x + 125
	# 		elif k in [19]:
	# 		#ll_ = lambda x: abs(x-129)
	# 		ll_ = lambda x: -x+129
	# 		elif k in [20]:
	# 		ll_ = lambda x: x + 55
	# 		else:
	# 		ll_ = lambda x: x		
	# 		ll[j][k] = ll_(ll[j][k])
	# 		"""
	try:
		rr = []
		for j in range(len(ll)-1):
			for k in range(len(ll[0])-1):
				#ll[j][k] = int(ll[j][k])
				#print "lala", ll[j][k]
				
				ff = ll[j][k].replace('[','')
				ff = ff.replace(']','')
				# print "%s adjustData params: (%s, %s)" % (source, k+1, ff)

				try:
					x = adjustData(k+1, num(ff))
				except ValueError:
					# print "%s adjustData() error!" % source
					pass
				# print x
				if x != '':
					ll[j][k] = x


		# print "%s updated ll: %s" % (source, ll)
		print "%s done!" % source
	except:
		print "%s something is wrong..." % source
			
	
# show the new element (no quotes)
	# print ll
	if [] in ll:
		ll.remove([])
	for l in ll:
		if '' in l: l.remove('')
		# print "%s len: %s" % (source, len(l))


# use zip(*<list-name>) to transpose list of list or tuples
#    print zip(*ll)[0]

	newll = []
	ll = zip(*ll)

	for m in ll:
		m = list(m)
	newll.append(m)

	# return zip(*ll)
	# print "%s new data: %s" % (source, newll)
	return newll

def num(s):
	try:
		return int(s)
	except ValueError:
		return float(s)
	 
def adjustData(idx, point):
	# print "%s idx: %s, point: %s" % (source, idx, point)
	if idx == 3 or idx == 6 or idx == 16:
		if point < -90:	return 0
		elif point > 90: return 180
		else: return point + 90		
	elif idx == 7 or idx == 8:
		if point > 0: return 180
		elif point < -180: return 0
		else: return point + 180
	elif idx == 9:
		if point > 90: return 180
		elif point < -90: return 0
		else: return point + 90
	elif idx == 13:
		if point > 9: return 99
		elif point < -90: return 0
		else: return point + 90
	elif idx == 14:
		if point > 51: return 180
		elif point < -129: return 0
		else: return point + 129
	elif idx == 15:
		if point < -125: return 0
		elif point > 55: return 180
		else: return point + 125
	#elif idx == 16:
	#	if point < -90:	return 0
	#	elif point > 90: return 180
	#	else: return point + 90
	elif idx == 17:
		if point > 90: return 180
		elif point < -32: return 32
		else: return point + 90
	elif idx == 19:
		if point < -19:	return 81
		elif point > 90: return 180
		else: return point + 90
	elif idx == 20:
		if point < -51: return 0
		elif point > 129: return 180
		else: return point + 51
	elif idx == 21:
		if point > 125:	return 180
		elif point < -55: return 0
		else: return point + 55
	elif idx == 22:
		if point > 90: return 180
		elif point < -90: return 0
		else: return point + 90
	elif idx == 23:
		if point < -90:	return 0
		elif point > 30: return 120
		else: return point + 90
	else: return point	
