import threading

def hello():
    print "Hello!"
def hi():
    print "hi"
t = threading.Timer(2, hello)
#p = threading.Timer(5)
t.start()
#p.start()
for i in range(10):
    #p.start()
    hi()

