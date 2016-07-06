import math

for i in range(len(data)-4):
    g = 0
    for j in range(len(kernel)):
	print data[i+j], kernel[j]
        g = data[i+j]*kernel[j]
	convolved.append(g)
    print "-------- total: ", g

# Kernel (based on indexing [-2, -1, 0, 1, 2]
kernel = [0.375, 0.25, 0.0625, 0.0625, 0.25]

# value of k: 0 <= k < fb
fb = int(math.log(frames,2))

# Padding data boundaries

for i in range(pow(2,k)):
    l = len(data)-1
    data[0:0] = [data[0]]
    data[l:l] = [data[l]]


# G1
for i in range(2,len(data)-2):
    g = 0
    for j in range(-2,3,1):
	print data[i+j], kernel[j]
	g += data[i+j]*kernel[j]
	convolved.append(g)
    print "-------- total: ", g

# G2
for i in range(4,len(data2)-4):
    g = 0
    for j in range(-2,3):
	print data2[i+2*j], kernel[j]
	g += data2[i+2*j]*kernel[j]
		
	convolved2.append(g)
    print "-------- total: ", g

#G3
for i in range(8, len(data3)-8):
    g = 0
    for j in range(-2,3):
        print data3[i+4*j], kernel[j]
        g += data3[i+4*j]*kernel[j]
        convolved3.append(g)
    print "-------- total:", g

for i in range(pow(2,k), len(data)-pow(2,k)):
    g = 0
    for j in range(-2,3,1):
        print data[i+(pow(2, k-1)*j)], kernel[j]
        g += data[i+(pow(2, k-1)*j)]*kernel[j]

        convolved[k].append(g)
    print "-------- total: ", g



    
