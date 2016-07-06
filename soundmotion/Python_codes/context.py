import time, re

class Context():
	def __init__(self):
		self.motions = []
		self.keywords = []
		self.actions = []
		self.motions = []
		self.history = []
		self.p1 = re.compile('i\'ll (dance|greet).$', re.I)
		self.p2 = re.compile('

	def updateContext(self, inputstring):
		
