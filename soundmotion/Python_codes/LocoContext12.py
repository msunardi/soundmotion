from LocoRegex import locoRegex
import random
from emotionModule import locoEmotion


#======================
# from pyLocoRobo_autoshynthesis2
#======================
class autoSynthesis:
	def __init__(self):
		from mosynth18_p import MotionSynthesizer
		import resampling, math, numpy
		
		self.ffunct = {'interpolate':self.interpolate, 'resample':self.resampleData2, 'modifygains':self.modifyGains, 'blend':self.concatMotion, 'waveshapefunct': self.waveshapef, 'waveshapegraph': self.waveshapeg}
		self.ffunctlist = [self.interpolate, self.interpolateAllMotions, self.resampling, self.resamplingAll, self.modifyGains, self.waveshapeftest, self.waveshapegtest, self.concatMotion, self.awareness]
		self.ms = MotionSynthesizer()
		self.resample = resampling.resample
		#self.fparam = {'motion': [],
		#			   'pose': [],
		#			   'motionbuffer': [],
		#			   'interp': {'bias': 0, 'tension': 0, 'continuity': 0},
		#			   'rate': 1,
		#			   'gains': [0,0,0],
		#			   'waveshapef': '',
		#			   'waveshapeg': [],
		#			   'awareness': {'orientation':"", 'position':"", 'target':""}}
		self.fparam = {'motionbuffer': [],
					   'pose': [],
					   'interpbias': [],
					   'interptension': [],
					   'interpcontinuity': [],
					   'rate': [],
					   'gains': [],
					   'filtered':[],
					   'gainslow': [],
					   'gainsmed': [],
					   'gainshigh': [],
					   'fftlow': [],					   
					   'ffthigh': [],
					   'waveshapef': [],
					   'waveshapeg': [],
					   'rcb1speed':[]}
		
		pass

	
	"""===readMotion(path):
		function: read .csv file from path
		input argument: path to .csv file (absolute)
		returns: motion in list format
		needs global variable(s): None
		affects global variable(s): None
	"""
	def readMotion(self, path):
		print "readMotion()...motion:", path, "...",
		try:		
			motion = self.ms.read(path)
			if motion:			
				#print "motion:",path,"loaded."
				print "loaded."
				#-print motion
				#return self.ms.read(path)
				return motion
			else: print "no motion loaded."
		except:
			print "error!"

	"""===setMotionbuffer(motion):
		function: store loaded motion to global variable fparam['motionbuffer']
		input argument: motion in list form (normally from/output of readMotion())
		returns: None
		needs global variable(s): None
		affects global variable(s): fparam['motionbuffer']
	"""
	def setMotionbuffer(self, motion):
		print "setMotions()...",
		try:
			self.fparam['motionbuffer'].append(motion)
			if self.fparam['motionbuffer']:
				print "fparam['motionbuffer'] is set. Length:", len(self.fparam['motionbuffer'])
				#-print self.fparam['motionbuffer']
			else: print "fparam['motionbuffer'] is not set."
		except:
			print "error!"
			return 0

	def countMotionbuffer(self):
		count = len(self.fparam['motionbuffer'])
		print "In Motionbuffer, there are", count, "motions."
		return count

	def getMotionbuffer(self):
		#-print "Retrieving Motionbuffer...", self.fparam['motionbuffer']
		return self.fparam['motionbuffer']

	def setPose(self, motion):
		print "setPose()...",
		try:
			self.fparam['pose'].append(motion)
			if self.fparam['pose']:
				print "fparam['pose'] is set. Length:", len(self.fparam['pose'])
				#-print self.fparam['pose']
			else: print "fparam['pose'] is not set."
		except:
			print "error!"
			return 0

	"""def setMotion(self, motion):
		print "setMotion()...",
		try:		
			if motion:
				self.fparam['motion'] = motion
				print "fparam['motion'] is set. Length:", len(self.fparam['motion'])
				print self.fparam['motion']
			else: print "fparam['motion'] is not set."
		except:
			print "error!"
			return 0
	"""
	"""===setAction():
		function: replaces setMotionbuffer, setMotion, and setPose -- because they have the same functionalities
		input argument: fparam index: {'motion', 'motionbuffer', 'pose'}, data: loaded motion
		returns: 1 if successful, 0 otherwise
		needs global variable(s): fparam
		affects global variable(s): fparam
	"""

	def setAction(self, storagetype, data):
		if storagetype not in ['motionbuffer', 'pose']:
			print "Invalid fparam index!"
			return 0
		
		print "set",storagetype,"...",
		try:
			self.fparam[storagetype].append(data)
			if self.fparam[storagetype]:
				print "fparam['"+storagetype+"'] is set.",
				if storagetype is 'motionbuffer':
					print "Length:", len(self.fparam['motionbuffer'])
					x = self.ms.multiresFiltering(data)					
					#self.fparam['gains'].append(self.ms.multiresFiltering(data))
					self.fparam['gains'].append(x)
					self.fparam['filtered'].append(self.ms.getFiltered())
					#-print "Gains:", x
				else: pass
				return 1
			else:
				print "fparam['"+storagetype+"'] is not set."
				return 0
		except:
			print "error!"
			return 0

	"""===clearMotion():
		function: clears the global variable fparam['motion']
		input argument: None
		returns: None
		needs global variable(s): None
		affects global variable(s): fparam['motion']
	"""
	"""def clearMotion(self):
		print "clearMotion()..."
		try:
			self.fparam['motion'] = []
			if len(self.fparam['motion']) == 0: print "cleared!"
			else: print "fparam['motion'] not empty."
		except:
			print "error!"
	"""
	"""===clearMotions():
		function: clears the global variable fparam['motionbuffer']
		input argument: None
		returns: None
		needs global variable(s): None
		affects global variable(s): fparam['motionbuffer']
	"""
	def clearMotionbuffer(self):
		print "clearMotionbuffer()..."
		try:
			self.fparam['motionbuffer'] = []
			if len(self.fparam['motionbuffer']) == 0: print "cleared!"
			else: print "fparam['motionbuffer'] not empty."
		except:
			print "error!"

	"""===setInterpTension(value):
		function: set the value for global variable fparam['interp']['tension'] (tension parameter for function interpolate())
		input argument: value (int) for global variable fparam['interp']['tension']
		returns: None
		needs global variable(s): None
		affects global variable(s): fparam['interp']['tension']
	"""
	def setInterpTension(self, value):
		print "Old Tension =", self.fparam['interptension'],
		#interpTension = value
		self.fparam['interptension'].append(value)
		print "new Tension =", self.fparam['interptension']

	"""===setInterpBias(value):
		function: set the value for global variable fparam['interp']['bias'] (bias parameter for function interpolate())
		input argument: value (int) for global variable fparam['interp']['bias']
		returns: None
		needs global variable(s): None
		affects global variable(s): fparam['interp']['bias']
	"""
	def setInterpBias(self, value):
		print "Old Bias =", self.fparam['interpbias'],
		#interpBias = value
		self.fparam['interpbias'].append(value)
		print "new Bias =", self.fparam['interpbias']

	"""===setInterpContinuity(value):
		function: set the value for global variable fparam['interp']['continuity'] (continuity parameter for function interpolate())
		input argument: value (int) for global variable fparam['interp']['continuity']
		returns: None
		needs global variable(s): None
		affects global variable(s): fparam['interp']['continuity']
	"""
	def setInterpContinuity(self, value): 
		print "Old Continuity =", self.fparam['interpcontinuity'],
		#interpContinuity = value
		self.fparam['interpcontinuity'].append(value)
		print "new Continuity =", self.fparam['interpcontinuity']

	def setRate(self, value):
		print "Old rate =", self.fparam['rate'],
		self.fparam['rate'].append(value)
		print "New rate =", self.fparam['rate']

	def setFparam(self, key, value):
		print "Old",key,"=", self.fparam[key],
		self.fparam[key].append(value)
		print "New",key,"=", self.fparam[key]

	def getFparam(self, key, index=None):
		#if index in ['interpbias', 'interptension', 'interpcontinuity','rate','gainslow', 'gainsmed', 'gainshigh']:
		try:
			if index is not None:
				print "Current",key,index,":",
				#-print self.fparam[key][index]
				return self.fparam[key][index]
			elif index is None:
				print "Current",key,"content:",
				#-print self.fparam[key]
				return self.fparam[key]
			#if index is 'interp':
			#	print sub_index,":", self.fparam[index][sub_index]
			#	return self.fparam[index][sub_index]
			#else:
			#	print ":", self.fparam[index]
			#	return self.fparam[index]
		#else:
		except:
			print "Invalid key or index!"
			return 0

	def setWaveshapef(self, expression):
		self.fparam['waveshapef'] = expression
		return 1

	def setWaveshapeg(self, waveshap):
		self.fparam['waveshapeg'] = waveshap
		
	"""===interpolate(motion):
		function: interpolate a single motion
		input argument: motion (2-D array/list) to be interpolated
		returns: interpolated motion
		needs global variable(s): fparam['motion'], fparam['interp']['bias', 'tension', 'continuity']
		affects global variable(s): None
	"""
	def interpolate(self, index=0, data=None):
		print "interpolate()...",
		try:
			if data is None:
				motion = self.fparam['motionbuffer'][index]
				#print "motionbuffer",index,":", motion
			else:
				motion = data
				#print "motion is:", motion
			
			print "bias:", self.fparam['interpbias'][index], "; tension:", self.fparam['interptension'][index], "; continuity:", self.fparam['interpcontinuity'][index]

			#interpolatedmotion = [ms.interpolate(m, fparam['interp']['bias'], fparam['interp']['tension'], fparam['interp']['continuity']) for m in fparam['motion']]
			interpolatedmotion = self.ms.interpolate(motion, self.fparam['interpbias'][index], self.fparam['interptension'][index], self.fparam['interpcontinuity'][index])
			return interpolatedmotion
		except:
			print "error!"
			return 0

	"""===interpolateAllMotions():
		function: interpolate each motion in fparam['motion'] separately.
			For example: if there are 3 motions in fparam['motion'], the result will be three interpolated motions in fparam['motion']
		input argument: None
		returns: None
		needs global variable(s): fparam['motionbuffer']
		affects global variable(s): fparam['motion']
	"""
	def interpolateAllMotions(self):
		print "interpolateAllMotions()..."
		try:
			#tmp = [interpolate(m) for m in self.fparam['motion']]
			self.fparam['motion'] = [self.ms.interpolate(m, self.fparam['interpbias'], self.fparam['interptension'], self.fparam['interpcontinuity']) for m in self.fparam['motionbuffer']]
			#self.fparam['motion'] = tmp
			#print "len(self.fparam['motion'])=", len(self.fparam['motion']), "fparam['motion']:", self.fparam['motion']
			return self.fparam['motion']
		except:
			print "error!"
			return 0

	"""===resampleData2():
		function: exterpolate motion data (i.e. resample - makes the motion faster)
		input argument: None
		returns: None
		needs global variable(s): fparams['rate'], motion data (tentatively: fparam['motion'])
		affects global variable(s): current motion data (tentatively: fprarm['motion'])
	"""
	def resampleData2(self):
		resample = resampling.resample
		#rate = ui.rateSpinBox.value()
		ui.rateSpinBox.setValue(fparams['rate'])
		new_data = []
		for data in self.ms.DATA:
			new_data.append(resample(data, rate))
		self.ms.multiresFiltering(new_data)
		#updatePlot()
		print "autosampling..."

	"""===resample(motion):
		function: extrapolate motion data
		input argument: one motion data
		returns: extrapolated motion data
		needs global var(s):
		affects global var(s):
	"""
	def resamplez(self, motion):
		print "resample()..."
		try:		
			tmp = [resample(data, self.fparam['rate']) for data in motion]
			if tmp:
				print "resampling successful."
				#print "tmp =", tmp
				return tmp
			else: print "resampling failed."
		except:
			print "error!"

	def resamplez2(self, motion, index):
		print "resample()...",
		#print "motion:", motion
		print "index:", index
		rate = self.fparam['rate'][index]
		print "rate:", rate
		try:		
			tmp = [self.resample(data, rate) for data in motion]
			if tmp:
				print "resampling successful."
				#print "tmp =", tmp
				return tmp
			else: print "resampling failed."
		except:
			print "error!"

	def resampling(self):
		return [resamplez(motion) for motion in self.fparam['motion']]

	def resamplingAll(self):
		return [resamplez(motion) for motion in self.fparam['motionbuffer']]

	"""===modifyGains():
		function: modify motion data by adjusting the gain values
		input argument: None
		returns: None
		needs global variable(s): fparam['gains']
		affects global variable(s): None
	"""
	def modifyGains(self):
		n = len(self.ms.countGains())
		#n = 9					   # static for test purposes...
		[start, step] = defstep(n)
		indices = range(start, n, step)
		for i in range(0,3):
			#setSliderValue(fparam['gains'][i], indices[i])
			print "fparam['gains'][", i, "]=", self.fparam['gains'][i], "; indices[", i,"]=", indices[i]

	def adjustGain(self, value, gainIndex):
		
		# === redraw
		self.tmpData = self.ms.DATA
		self.ms.DATA = self.ms.interpolate(self.originalData, self.interpBias, self.interpTension, self.interpContinuity)
		self.ms.multiresFiltering(self.ms.DATA)
		for i in range(self.ms.countGains()):
			for channel in range(self.channels):
				# === if it's not the changed slider...
				if i != gainIndex:
				
					self.ms.adjustGain(channel, i, self.ui.gainSliders[i].value()*0.1)
					self.ui.gainLineEdits[i].setText(str(self.ui.gainSliders[i].value()*0.1))
							
				# === otherwise, it's the changed slider	
				else:

					self.ms.adjustGain(channel, gainIndex, value*0.1)
					self.ui.gainLineEdits[gainIndex].setText(str(self.ui.gainSliders[gainIndex].value()*0.1))
					self.ui.statusbar.showMessage("Band "+self.ui.gainSliders[gainIndex].accessibleName()+" gain changed to "+ str(value*0.1))
				

		self.updatePlot()
		
		print "Sender: %s, value: %f" % (self.sender().accessibleName(), self.sender().value()*0.1)#, self.tmpData[channel]
		self.ms.DATA = self.ms.returnNewData()

	def adjustGain2(self, data, gains, gainslow=1, gainsmed=1, gainshigh=1):   #<< see modifyGains(self) above
		print "adjustGain2...",
		try:
			#print "gains:",gains
			#-self.ms.setGains(gains)
			#print "DATA:",data
			#-self.ms.setDATA(data)
			self.ms.multiresfiltering(data)
			newgains = []
			n = len(gains[0])
			gainadjustments = [gainslow, gainsmed, gainshigh]
			print "gainadjustments:", gainadjustments

			[start, step] = self.defstep(n)
			indices = range(start, n, step)
			for i in range(0,3):
				for channel in range(len(data)):
					#Trouble with adjustGain2 resolved (6/22): indices parameter need index [i]: indices >> indices[i]
					self.ms.adjustGain(channel, indices[i], gainadjustments[i])
			print "done!"
			return 1
		except:
			print "failed."
			return 0

	def adjustGain3(self, index):   #<< see modifyGains(self) above
		print "adjustGain3...",
		try:
			#print "gains:",gains
			#-self.ms.setGains(gains)
			#print "DATA:",data
			#-self.ms.setDATA(data)
			data = self.fparam['motionbuffer'][index]
			gains = self.fparam['gains'][index]
			gainslow = self.fparam['gainslow'][index]
			gainsmed = self.fparam['gainsmed'][index]
			gainshigh = self.fparam['gainshigh'][index]
			filtered = self.fparam['filtered'][index]
			self.ms.setDGF(data, gains, filtered)
			
			newgains = []
			n = len(gains[0])
			gainadjustments = [gainslow, gainsmed, gainshigh]
			print "gainadjustments:", gainadjustments

			#Just select 3 frequency bands that represent the high, medium, and low frequencies
			#The gain adjustments are only applied to these frequencies
			#Assumption: adjusting neighboring frequency band gains won't have substantial difference...
			# ...from adjusting these 'representative' band gains.
			[start, step] = self.defstep(n)
			indices = range(start, n, step)
			for i in range(0,3):
				for channel in range(len(data)):
					#Trouble with adjustGain2 resolved (6/22): indices parameter need index [i]: indices >> indices[i]
					#channel type: int, indices type: int, gainadjustments type: int/float
					self.ms.adjustGain(channel, indices[i], gainadjustments[i])
			print "done!"
			return 1
		except:
			print "failed."
			return 0

	"""===defstep(x):
		function: given x number of gains, find the low, medium, high gain indices
		input argument: x (i.e. number of gains)
		returns: initial index, steps
		needs global variable(s): None
		affects global variable(s): None
	"""
	def defstep(self, x):
		s = x%3
		f = x/3
		if s > 1:
			return f-1, f+1
		else:
			return f-1, f

	"""===concatMotion():
		function: combine the motions in fparam['motionbuffer'] sequentially into one
		input argument: None
		returns: concatenated (combined) motion
		needs global variable(s): fparam['motionbuffer']
		affects global variable(s): None
	"""
	def concatMotion(self):
		print "concatMotion()...",
		try:
			if len(self.fparam['motionbuffer']) >= 2:
				concatenated = reduce(lambda m1, m2: self.ms.concatenatemotion(m1,m2), self.fparam['motionbuffer'])
				if concatenated:
					setMotion([concatenated])
					print "motions concatenated. Inserted to fparam['motion']"
					#print "concatenated motion:", concatenated
					return concatenated			
				else: print "concatenation failed."
			else:
				print "Need 2 or more motions to concatenate."
				return 0
		except:
			print "error!"
			return 0

	def concatMotion2(self, motion1, motion2):
		print "concatMotion()...",
		try:
			motions = [motion1, motion2]
			concatenated = reduce(lambda m1, m2: self.ms.concatenatemotion(m1,m2), motions)
			if concatenated:
				#setMotion([concatenated])
				print "motions concatenated."
				#print "concatenated motion:", concatenated
				return concatenated			
			else:
				print "concatenation failed."
				return 0
			
		except:
			print "error!"

	def concatMotion3(self, motions):
		print "concatMotion()...",
		try:
			print "motion lengths:", len(motions)
			#motions = [motion1, motion2]
			concatenated = reduce(lambda m1, m2: self.ms.concatenatemotion(m1,m2), motions)
			if concatenated:
				#setMotion([concatenated])
				print "motions concatenated."
				#print "concatenated motion:", concatenated
				return concatenated			
			else:
				print "concatenation failed."
				return 0
			
		except:
			print "error!"
			return 0
				
	"""===superpose():
		function: combine/blend two motions into one (currently can't be done properly when the lengths of the two motions are different)
		input arguments: motion1 and motion2 -- the two motions to be combined
		returns: None
		needs global variable(s): None
		affects global variable(s): None (if working, current motion)
	"""
	def superpose(self, motion1, motion2, m2weight=0.1):
		try:
		#if True:
			tmp = []
			#data = ms.returnNewData()
			print "Superpose...",
			l1 = len(motion1[0])
			l2 = len(motion2[0])
			try:
				import numpy
			#if True:
				if l1 > l2:
					#print "motion 1 is longer than motion2. l1=",l1,", l2=",l2
					#print "motion2:", motion2
					m2 = numpy.array(motion2)					
					m2 = m2.repeat(l1,1)
					#print m2
					
			except:
				print "motion2 matching failed."

			for i in range(len(motion1)):
				try:
					#tmpData = list(numpy.add(motion1[i], numpy.multiply(motion2[i], 0.5)))
					tmpData = list(numpy.add(motion1[i], numpy.multiply(m2[i], m2weight)))
					#ui.statusbar.showMessage("Superposing...")
					
				except:
					#print "length data: ", len(data[i]), "points = ", len(new_points)
					#ui.statusbar.showMessage("Waveshape 2 failed.")
					print "failed!"
				tmp.append(tmpData)
				#ui.qwtPlot.changeCurve(i, tmpData)

			#newData = tmp
			self.ms.DATA = tmp
			
			print "done!"
			return tmp
				
		except:
			#ui.statusbar.showMessage("Uh oh, something is wrong...")
			print "Uh oh, something is wrong..."
			return 0

	"""===waveshapef():
		function: creates a waveshaping waveform using a function in fparam['waveshapef']
		input arguments: None
		returns: None
		needs global variable(s): fparam['waveshapef']
		affects global variable(s): Currently none (should be: fparam['motion'])
	"""
	def waveshapef(self):
		try:
			text = unicode(self.fparam['waveshapef'])
			#x = 2
			ui.statusbar.showMessage("Auto-Waveshaping function(x) = %s" % (text))
			c = 0
			y = []

			currentData = self.ms.returnNewData()
			for x in range(len(currentData[0])):
				c = eval(text)
				y.append(c)				
				c = 0			

			#print "y: ", y

			# == Normalize
			for i in range(len(y)):
				y[i] = float(y[i])/max(y)

			#print "new y: ",y
			
		except:
			ui.statusbar.showMessage("%s is invalid!" % text)

		plotExp(ui.expPlot, range(len(currentData[0])), y)
		applyWaveshapef()

	def waveshapeftest(self):
		print "waveshapeftest...",
		try:
			print "ok."
			for x in range(10):
				print eval(self.fparam['waveshapef'])
		except:
			print "meh."

	"""===applyWaveshapef():
		function: applying waveshaping function from waveshapef() to motion data
		input arguments: None
		returns: None
		needs global variable(s): None
		affects global variable(s): Currently none (should be: fparam['motion'])
	"""
	def applyWaveshapef(self):
		multiplier = 0.15
		try:
			tmp = []
			data = self.ms.returnNewData()

			for i in range(len(data)):
				tmpData = list(numpy.add(data[i], numpy.multiply(data[i], numpy.multiply(y, multiplier))))
				tmp.append(tmpData)
				ui.qwtPlot.changeCurve(i, tmpData)

			#newData = tmp
			self.ms.DATA = tmp
			ui.expSpinBox.setValue(multiplier)
				
		except:
			ui.statusbar.showMessage("Uh oh, something is wrong...")

	"""==waveshapeg():
		function: creates a waveshaping function by manually editing points of the waveshaping wave
		input arguments: None
		returns: None
		needs global variable(s): fparam['waveshapeg'] i.e. list of pairs of point indices, values of corresponding point
		affects global variable(s): None
	"""
	def waveshapeg(self):  # derived from pointChange(...)
		try:
			print "Applying waveshapeg"
			
			for p in self.fparam['waveshapeg']:
				points[p[0]] = p[1] * 0.1
			#print "value in point ", currentPointIndex, "= ", points[currentPointIndex]
			print "points = ", points
			new_points = self.ms.interpolate2(points)
			#print "interpolated points: ", new_points
			plotWave(ui.wavePlot, range(len(new_points)), new_points)
		except:
			print "Waveshapeg failed..."

	def waveshapegtest(self):
		print "waveshapeg...",
		try:
			print "ok."
			points = numpy.zeros(10)
			for p in self.fparam['waveshapeg']:
				points[p[0]] = p[1]*0.1
			print "points = ", points
		except:
			print "epic fail."
			
	"""def plotWave( target, x, y):   # >>> this is similar to plotExp
		waveCurve = Qwt.QwtPlotCurve("waveCurve")
		waveCurve.setPen(Qt.QPen(Qt.Qt.red))
		waveCurve.setData(x, y)
		ui.wavePlot.clear()
		waveCurve.attach(target)
		ui.wavePlot.replot()   """

	def awareness(self):
		pass

	def applyAll(self):
		for i in range(len(self.fparam['motionbuffer'])):
			pass
		return 0


	def resetFparam(self):
		self.fparam = {'motionbuffer': [],
					   'pose': [],
					   'interpbias': [],
					   'interptension': [],
					   'interpcontinuity': [],
					   'rate': [],
					   'gains': [],
					   'filtered': [],
					   'gainslow': [],
					   'gainsmed': [],
					   'gainshigh': [],
					   'fftlow': [],					   
					   'ffthigh': [],
					   'waveshapef': [],
					   'waveshapeg': []}
		print "fparam reset!"
		return 1

	def returnNewMotion(self):
		return self.ms.returnNewData()
				

"""emotions:(mad|angry|happy|sad|afraid|worried|tired|bored|fine|joyful|disgruntled|dissastisfied|disturbed)
   verbs:(relax|laugh|cry|talk|walk|run|jump|hit|bow|pick|fall|fly|swim|golf|pushup|dance)

"""
class locoContext:

	def __init__(self):
		""" motionordervar format:
			fparam = {'motion': [],
			'motionbuffer': [],
			'interp': {'bias': 0, 'tension': 0, 'continuity': 0},
			'rate': 1,
			'gains': [0,0,0],
			'waveshapef': '',
			'waveshapeg': [],
			'awareness': {'orientation':"", 'position':"", 'target':""}}
		"""
		
		self.em = locoEmotion()
		self.asyn = autoSynthesis()
		self.motionFilePath = {'pushup':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv",
							   'backflip':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backflip.csv",
							   'backroll':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backward_roll.csv",
							   'dance2':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/dance2.csv",
							   'fly':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/flying.csv",
							   'walk':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/goodwalk.csv",
							   'home':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/home.csv",
							   'karatekid':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/karatekid.csv",
							   'pose_angry':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_angry.csv",
							   'pose_cocky':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_cocky.csv",
							   'pose_relax':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_relax.csv",
							   'pose_surprised':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_surprised.csv",
							   'pose_tired':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_tired.csv",
							   'pulsing':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/pulsing.csv",
							   'pulsing2':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/pulsing2.csv",
							   'pulsing3':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/pulsing3.csv",
							   'wave_r_arm':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/wave_right_arm.csv",
							   'weirdgesture1':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/weirdarmgesture.csv",
							   'weirdgesture2':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/weirdarmgesture2.csv",
							   'se_leftright':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_swing_leftright.csv",
							   'se_bird':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_bird.csv",
							   'se_surfleft':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_left.csv",
							   'se_surfright':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv",
							   'cartwheel':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/cartwheel.csv",
							   'extrm_ch1:':"/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH1.csv"}  # <<< Selected motion signals
		
		self.lr = locoRegex()
		self.homePos = self.asyn.readMotion(self.motionFilePath['home'])
		self.outputmotion = []
		self.userinput = ''

	def lcKeywords(self, inputstring, userinput):
		print "get lcKeywords..."
		(self.miscverb, self.roboemotion, self.robokeyverb, self.topic, xname, self.roboemo) = self.lr.matchRule(inputstring)
		(self.usermiscverb, self.emotion, self.keyverb, self.usertopic, self.userwrongname, useremo) = self.lr.matchRule(userinput)
		
		self.userinput = userinput
		self.robotresponse = inputstring
		self.wrongname()
		
		#self.getEmo(self.emo)
		self.emotion = self.emotion[1]
		print "user input:", userinput
		print "USER: miscverb:", self.usermiscverb, ", emotion:", self.emotion, ", keyverb:", self.keyverb, ", topic:", self.usertopic
		print "USER: miscverb: %s, emotion: %s, keyverb: %s, topic: %s" % (self.usermiscverb, self.emotion, self.keyverb, self.usertopic)
		
		print "robot response:", inputstring		
		print "ROBOT: miscverb:", self.miscverb, ", emotion:", self.roboemotion, ", keyverb:", self.robokeyverb, ", topic:", self.topic
		
		return 1
		
	#Messing around with EmotionModule...
	def getEmo(self, emotions):
		print "getEmo..."
		if len(emotions) == 4:
			levels = [self.em.emoLevel(e) for e in emotions] # expect only 4 elements in emotions
			self.em.alterEmo(levels[0],levels[1],levels[2],levels[3])
			print "levels: ", levels
		else:
			self.em.alterEmo(0,0,0,0)
		self.emoIntensity = self.em.getEmoIntensity()
		self.emoActionProbability = self.em.getProbAction()
		(self.eContinuity, self.eTension, self.eBias, self.eRate, self.eHighGain, self.eMedGain, self.eLowGain) = self.em.getEmoParam()
		print self.emoIntensity, self.emoActionProbability, self.eContinuity, self.eTension, self.eBias, self.eRate, self.eHighGain, self.eMedGain, self.eLowGain
		
	def wrongname(self):
		print "wrong name?"
		if self.userwrongname:
			return True
		else:
			return False	

	def updateContext(self):
		self.asyn.resetFparam()
		update = False
		if self.keyverb is not None or self.emotion is not None or self.miscverb is not None:
			update = True
			print "Context update...",
			if self.keyverb == 'relax':
				#invoke (push to pose) relax pose
				#self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_relax']))
				self.updateFparam(pose=self.asyn.readMotion(self.motionFilePath['pose_relax']))
				
			if self.keyverb == 'wave':
				action = self.asyn.readMotion(self.motionFilePath['wave_r_arm'])
				par=[0,0,0,1,1,1,1]
				if self.emotion == 'happy':
					par=[3,-2,-1,3,1.,3,1]
				elif self.emotion == 'afraid':
					par=[-1,4,0,1,2,-0.5,1]
				elif self.emotion == 'sad':
					par=[2,-2,1,1,1,1,1]
				elif self.emotion == 'angry':
					par=[-2,4,2,10,1,1,1.5]
				self.updateFparam(motionbuffer=action, interpcontinuity=par[0],interptension=par[1],interpbias=par[2],rate=par[3],gainshigh=par[4],gainsmed=par[5],gainslow=par[6])
			elif self.keyverb == 'walk':
				#invoke (push to motionbuffer) walk action
				#self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['walk']))
				self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['walk']))
				
			elif self.keyverb == 'dance':				
				#invoke dance action
				#-self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['dance2']))
				if self.emotion == 'happy':
					self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['dance2']),
									  rate=7,
									  interpcontinuity=1,
									  interptension=-1,
									  gainsmed=3)
				else:
					self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['pose_relax']))
				
			elif self.keyverb == 'fly':				
				#invoke fly action
				#-self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['fly']))
				self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['fly']))

			elif self.keyverb == 'pushup':
				#invoke pushup action
				#self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['pushup']))
				if self.emotion == 'tired' or self.emotion == 'sad':
					self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['pushup']),
									  gainsmed=-2,
									  gainslow=-2,
									  interpbias=2)
				else:
					self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['pushup']))

			elif self.keyverb == 'fight':
				#invoke fighting action
				#--self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_angry']))
				#--self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['karatekid']))
				#--self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['weirdgesture1']))
				concatmotion = self.asyn.concatMotion2(self.asyn.readMotion(self.motionFilePath['karatekid']),self.asyn.readMotion(self.motionFilePath['weirdgesture1']))
				#-self.updateFparam(pose=self.asyn.readMotion(self.motionFilePath['pose_angry']), motionbuffer=self.asyn.readMotion(self.motionFilePath['karatekid']))
				#-self.updateFparam(pose=self.asyn.readMotion(self.motionFilePath['pose_angry']), motionbuffer=self.asyn.readMotion(self.motionFilePath['weirdgesture1']))
				self.updateFparam(motionbuffer=concatmotion, 
				#				  pose=self.asyn.readMotion(self.motionFilePath['pose_angry']),
								  interpcontinuity=-1,
								  interpbias=2,
								  rate=5)
				

			if self.emotion == 'mad' or self.emotion == 'angry':
				print "mad / angry: set angry pose, sampling rate=3, gain++, interp tension++"
				
				#set angry pose
				#self.asyn.setMotionbuffer(self.asyn.readMotion(self.motionFilePath['pose_angry']))
				#-self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_angry']))
				
				#set (sampling) rate = 3
				#-self.asyn.setRate(3)
				
				#set gain ++ (higher)
				#-self.asyn.getFparam('gainslow')
				#-self.asyn.getFparam('gainsmed')
				#-self.asyn.getFparam('gainshigh')
				
				#set interp tension ++ (higher)
				#-self.asyn.getFparam('interptension')
				#-self.asyn.setInterpTension(1)
				#self.updateFparam(interptension=1, rate=5, pose=self.asyn.readMotion(self.motionFilePath['pose_angry']))
				self.updateFparam(interptension=1, rate=3, motionbuffer=self.asyn.readMotion(self.motionFilePath['pose_angry']))
				
			elif self.emotion == 'happy' or self.emotion == 'joyful':
				print "happy / joyful: set sampling rate=3, gain++, interp continuity++, tension--"
				
				#set (sampling) rate = 3
				self.asyn.getFparam('rate')
				#-self.asyn.setRate(3)
				
				#set gain ++
				self.asyn.getFparam('gainsmed',0)
				
				#set interp continuity ++, tension -- (less) or more?
				#-self.asyn.getFparam('interpcontinuity')
				#-self.asyn.getFparam('interptension')
				#-self.asyn.setInterpContinuity(2)
				#-self.asyn.setInterpTension(1.5)

				self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['se_bird']),
								  rate=5,
								  gainsmed=0,
								  interpcontinuity=1,
								  interptension=1)
				
			elif self.emotion == 'sad' or self.emotion == 'tired' or self.emotion == 'bored' and self.keyverb is None:
				print "sad / tired / bored: set tired pose, gain--"
				
				#set tired pose
				#-self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_tired']))
				
				#set gain --
				self.asyn.getFparam('gainslow')
				self.asyn.getFparam('gainsmed')
				self.asyn.getFparam('gainshigh')

				self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['pose_relax']),
								  gainslow=-2,
								  gainsmed=-1)
				#				  gainshigh=-1)
				#self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['home'])
				#				  pose=self.asyn.readMotion(self.motionFilePath['pose_tired']),
				#				  gainslow=0,
				#				  gainsmed=-10,
				#				  gainshigh=-10)

			elif self.emotion == 'calm':
				#self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['se_surfright']))
				#self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['se_surfleft']))
				
				#-self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['se_surfright']))
				#-self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['se_surfleft']))
				#-self.asyn.concatMotion()

				#concatmotion = self.asyn.concatMotion2(self.asyn.readMotion(self.motionFilePath['se_surfright']),self.asyn.readMotion(self.motionFilePath['se_surfleft']))
				concatmotion = self.asyn.concatMotion2(self.asyn.readMotion(self.motionFilePath['se_surfright']),self.asyn.readMotion(self.motionFilePath['pose_relax']))
				
				
				self.updateFparam(motionbuffer=concatmotion,
								  gainshigh=-1,
								  interpcontinuity=2,
								  interptension=-1)
				#self.updateFparam(motionbuffer=concatmotion)
				#self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['se_surfright']))
			else:
				
				print "update", update
			
		else:
			
			print "update", update
		return update
	
	def updateContext2(self):	# with emotion!
		self.asyn.resetFparam()
		self.getEmo(self.roboemo)	# << see?
		update = False
		if self.keyverb is not None or self.emotion is not None or self.miscverb is not None:
			update = True
			pose = None
			action = None
			#action = self.asyn.readMotion(self.motionFilePath['home'])
			print "Action update...",
			if self.keyverb == 'relax':
				#invoke (push to pose) relax pose
				print "relax pose..."
				action=self.asyn.readMotion(self.motionFilePath['pose_relax'])
				
			elif self.keyverb == 'walk':
				print "walking..."
				#invoke (push to motionbuffer) walk action
				#self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['walk']))
				action=self.asyn.readMotion(self.motionFilePath['walk'])
				
			elif self.keyverb == 'dance':
				print "dancing..."
				#invoke dance action
				action=self.asyn.readMotion(self.motionFilePath['dance2'])
				
			elif self.keyverb == 'fly':
				print "flying..."						
				#invoke fly action
				#-self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['fly']))
				action=self.asyn.readMotion(self.motionFilePath['fly'])

			elif self.keyverb == 'pushup':
				print "pushup..."
				#invoke pushup action
				action=self.asyn.readMotion(self.motionFilePath['pushup'])

			elif self.keyverb == 'fight':
				action=self.asyn.concatMotion2(self.asyn.readMotion(self.motionFilePath['karatekid']),self.asyn.readMotion(self.motionFilePath['weirdgesture1']))
				

			if self.emotion == 'mad' or self.emotion == 'angry':
				print "mad / angry: set angry pose, sampling rate=3, gain++, interp tension++"				
				
				action=self.asyn.readMotion(self.motionFilePath['pose_angry'])
				
			elif self.emotion == 'happy' or self.emotion == 'joyful':
				print "happy / joyful: set sampling rate=3, gain++, interp continuity++, tension--"
				
				action=self.asyn.readMotion(self.motionFilePath['se_bird'])
								  
				
			elif self.emotion == 'sad' or self.emotion == 'tired' or self.emotion == 'bored' and self.keyverb is None:
				print "sad / tired / bored: set tired pose, gain--"
				
				#set tired pose
				#-self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_tired']))
				
				#set gain --
				self.asyn.getFparam('gainslow')
				self.asyn.getFparam('gainsmed')
				self.asyn.getFparam('gainshigh')

				action=self.asyn.readMotion(self.motionFilePath['pose_relax'])


			elif self.emotion == 'calm':
				
				action = self.asyn.concatMotion2(self.asyn.readMotion(self.motionFilePath['se_surfright']),self.asyn.readMotion(self.motionFilePath['pose_relax']))								
				
			else:
				
				print "update", update
			
			ra = random.random()
			print "Random: %f vs. ProbAction: %f" % (ra, self.emoActionProbability)
			if ra < self.emoActionProbability:
				print "OK, I'll do this..."
				if action is not None:
					self.updateFparam(motionbuffer=action, interpbias=self.eBias, interptension=self.eTension, interpcontinuity=self.eContinuity, rate=int(self.eRate), gainshigh=self.eHighGain, gainsmed=self.eMedGain, gainslow=self.eLowGain)
				else: print "no motion to execute..."
			else:
				print "ZZZZ..."
		else:
			
			print "update", update
		return update
	

	def updateFparam(self, motionbuffer=None, pose=None, interpbias=0, interptension=0, interpcontinuity=0, rate=1, gainslow=1, gainsmed=1, gainshigh=1, fftlow=1, ffthigh=1):
		
		#if pose is None:
			#pose = self.asyn.readMotion(self.motionFilePath['pose_relax'])
		#	pose = self.asyn.readMotion(self.motionFilePath['home'])
		self.asyn.setAction('pose', pose)		
		self.asyn.setInterpBias(interpbias)
		self.asyn.setInterpTension(interptension)
		self.asyn.setInterpContinuity(interpcontinuity)
		self.asyn.setFparam('gainslow', gainslow)
		self.asyn.setFparam('gainsmed', gainsmed)
		self.asyn.setFparam('gainshigh', gainshigh)
		self.asyn.setRate(rate)
		if motionbuffer is None:
			motionbuffer = self.asyn.readMotion(self.motionFilePath['home'])
		interpolatedmotionbuffer = self.asyn.interpolate(index=-1,data=motionbuffer) #<< resolved *whew* missing index for each interp parameters in ms.interpolate
		#Do setAction('motionbuffer', ...) after the interpolation parameters are set
		self.asyn.setAction('motionbuffer', interpolatedmotionbuffer)
		return 1				

	def getMotionResponse(self):
		print "getMotionResponse()"	#Test
		#process/apply everything (just pick an order)
		#return self.asyn['motion']

	def loadMotion(self, index):
		try:
			path = self.motionFilePath[index]
			print "path:", path
			self.asyn.readMotion(path)
			return 1
		except:
			print "loadMotion failed.  Check if index is correct (",index,") and the motion exist."
			return 0

	def checkMotionbuffer(self):
		self.asyn.countMotionbuffer()
		return 1

	###===+++*** THIS IS THE BIG FUNCTION THAT APPLIES ALL TRANSFORM FUNCTION FOR EACH MOTION IN MOTIONBUFFER!!!
	""" === How it works:
			1. Each element in motionbuffer is processed individually:
				1.1 Adjust gains of the ORIGINAL DATA according to values of: gainslow, gainsmed, gainshigh
				1.2 Since the effect of gain adjustments are done implictly in mosynth_##, invoke returnNewMotion() to retrieve the adjusted motion
				1.3 Interpolate the new data
				1.4 Superpose the new data with the pose
				1.5 Resample the new-superposed data, if applicable
				1.6 ... apply other transformations, if any
				1.7 Add the adjusted data for this motionbuffer element to the tmp container
				1.8 repeat for the next element in motionbuffer
			2. After all elements are adjusted, the tmp container should be full of sequences of motions.
			3. Concatenate all the sequences in tmp into one big motion
			4. Return the concatenated, final motion.

	"""
	def executeAllMotion(self):
		tmp = []
		print "LocoContext.executeAllMotion()...",
		for index in range(len(self.asyn.getFparam('motionbuffer'))):
			#apply gain adjustments to each_motion (original data) << be careful about this...
			try:
				#self.asyn.adjustGain2(data=self.asyn.getFparam('motionbuffer',index),
				#					  gains=self.asyn.getFparam('gains',index),
				#					  gainslow=self.asyn.getFparam('gainslow',index),
				#					  gainsmed=self.asyn.getFparam('gainsmed',index),
				#					  gainshigh=self.asyn.getFparam('gainshigh',index))
				self.asyn.adjustGain3(index)
			except:
				print "Trouble in adjustGain3!"
				return 0
			
			#get the new gain-adjusted data
			try:
				tmp1 = self.asyn.returnNewMotion()
			except:
				print "Trouble in returnNewMotion!"
				return 0
			#interpolate each_motion
			try:
				#tmp2 = self.asyn.interpolate(data=tmp1)
				tmp2 = tmp1
			except:
				print "Trouble in interpolate!"
				return 0
			#superpose with pose
			try:
			#if True:
				#tmp3 = self.asyn.superpose(tmp2, self.asyn.getFparam('pose',index))
				tmp3 = tmp2
			except:
				print "Trouble in superpose!"
				return 0
			#print "tmp3 =",tmp3
			#apply resample, if any
			try:
				print "resampling...",
				rate=self.asyn.getFparam('rate',index)
				print len(tmp3)
				if rate is not 1:
					#-print tmp3
					#-print index
					tmp4 = self.asyn.resamplez2(tmp3, index)
				else:
					print "rate = 1, not resampling."
					tmp4 = tmp3
			except:
				print "Trouble in resamplez2!"
				tmp4 = tmp3
				return 0
			#apply other transformations, if any
			print "len tmp4:",len(tmp4)

			tmp.append(tmp4)
											
			#pass
		#concatenate all the transformed motion		
		#save the concatenated motion
		#print "tmp=",tmp
		if tmp is None or tmp==[]:
			print "WARNING! tmp is empty"
		try:
			self.outputmotion = self.asyn.concatMotion3(tmp)
			if self.outputmotion == 0:
				print "FAIL!"
				self.asyn.resetFparam()
				return 0
			else:
				print "SUCCESS!!!"
				self.asyn.resetFparam()				
				return self.outputmotion
			
		except:
			print "Trouble in concatMotion2!"
			self.asyn.resetFparam()
			return 0

		

#======================
# Test LocoContext
#======================

#-lc = locoContext()
#lc.lcKeywords("i dance and i'm mad")
#-lc.lcKeywords("when i dance, i'm calm")
#lc.getMotionResponse()
#-lc.updateContext()
#-lc.executeAllMotion()
#lc.loadMotion('pose_angry')
#lc.checkMotionbuffer()
#lc.lcKeywords("I'm tired")
#lc.updateContext()
#lc.checkMotionbuffer()
