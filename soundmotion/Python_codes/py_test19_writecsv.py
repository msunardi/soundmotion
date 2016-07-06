import csv
import sys
writer = csv.writer(open("test.csv", "wb"))

j = [[1,2,3],[3,4,5]]

writer.writerows(j)
