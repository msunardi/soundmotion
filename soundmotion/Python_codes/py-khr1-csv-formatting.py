import csv

def khr1CsvFormatting( csv_source ):
    # setting up list variables
    l = []
    ll = []

    # read .csv file and populate list
    for line in csv.reader(open( csv_source ).readlines()[1:]):
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
    #print zip(*ll)[0]

    return zip(*ll)

print khr1CsvFormatting( "/home/msunardi/Documents/KHR-1-motions/push_ups_data.csv" )
