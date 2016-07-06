class listcomp:

    def __init__(self):
        self.list = [self.f1, self.f2, self.f3]

    def f1(self, x):
        x +=1
        print "f1",x
        return x

    def f2(self, y):
        y += 1
        print "f2",y
        return y

    def f3(self, z):
        z += 1
        print "f3",z    
        return z
        
    def createlist(self, order):
        flist = [self.list[i] for i in order]
        #for f in flist:
        #    f()
        return flist


lc = listcomp()
#lc.createlist([0,1,2])
#lc.createlist([2,0,1])
#for f in lc.createlist([1,0,2]):
#    f()

reduce(lambda x, y: y(x), lc.createlist([0,2,1]), 1)
