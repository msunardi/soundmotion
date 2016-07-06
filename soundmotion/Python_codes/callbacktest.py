import speechd, time

called = []
client = speechd.SSIPClient('callback-test')
client.speak("hello there!", callback = lambda cb_type: called.append(cb_type))
time.sleep(2)
print "Called callbacks:", called
client.close()
