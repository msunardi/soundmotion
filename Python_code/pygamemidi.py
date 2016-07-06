import pygame.midi as pm

#print "x", help(pygame.midi)

print "pm init ...", 
try:
	pm.init()
	print "success"
except:
	print "failed"

