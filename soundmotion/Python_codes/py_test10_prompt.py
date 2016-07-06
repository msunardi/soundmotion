ans = raw_input('ngeks> ')

if not ans:
    pass

args = ans.split()
for g in args:
    print g

if 'halo'.find(args[0]) == 0:
    print args[0]
    print args[1]
