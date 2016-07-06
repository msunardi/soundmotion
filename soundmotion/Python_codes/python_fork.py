import os

pid = os.fork()
if pid == 0:
  print "I'm child pid=", pid, " real pid=", os.getpid()
else:
  print "I'm parent. Child pid=", pid, " my pid=", os.getpid()

