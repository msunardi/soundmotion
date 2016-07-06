import math

g = lambda x: 0.5*x+2

print g(2)

#---- lambda function in a list

list = [g]

print list[0](2)

h = lambda x: g(2)*x

list.append(h)

print list[1](1)

j = lambda x: 1

print j(100)

def truncated(p1, p2, p3, p4):
    a = 1/p2
    b = -1/abs(p4-p3)
    f0 = lambda x: a*x
    
    f1 = lambda x: 1

    f2 = lambda x: b*x+1

    trunc = [f0,f1,f2]

    return trunc

eg = truncated(0, 4, 4, 8)

    
print eg[1](10325)
    
