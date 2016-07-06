class myClass:

    def __init__(self, param1=None, param2=None):
        self.par1 = param1
        self.par2 = param2

    def printParams (self):
        print self.par1, self.par2
        for i in [1,2]:
            print "a",

""" ==================
    test
    ==================
"""


j = myClass(3, 2)
j.printParams()


