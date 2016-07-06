import sys, os, threading, signal

i = 0

#threading.Thread(os.execvp("python", ["python", "/home/msunardi/Python-project/pymedia_allplayer.py",  "/home/msunardi/Music/02-4Minutes.mp3"]))

pid = os.fork()

if pid > 0:
	os.system("python /home/msunardi/Python-project/pymedia_allplayer.py /home/msunardi/Music/02-4Minutes.mp3")
	print "I'm done\n"
else:
	i = 0
	while True:
		print "playing...", i
		i = i + 1
		if i > 500000:
			os.kill(pid, signal.SIGKILL)
			sys.exit(0)
			


