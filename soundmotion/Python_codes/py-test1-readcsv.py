import csv

l = []

for line in csv.reader(open("/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv").readlines()[1:]):
    l.append(line)

print l[0][3:]
