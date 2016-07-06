import csv

l = []
ll = []
for line in csv.reader(open("/home/msunardi/Documents/KHR-1-motions/push_ups_data.csv").readlines()[1:]):
    l.append(line)

for inline in line:
    ll.append(line[:][3:])

