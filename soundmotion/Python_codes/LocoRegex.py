import re

class locoRegex:

	def __init__(self):
		#self.pat1 = re.compile('(\S+\s+)*I\s+(\w+)', re.IGNORECASE)
		self.pat1 = re.compile('(\S+\s+)*I\s+^(like|feel|can|have|will|should|would|could|did|do|seem|suppose)*\s+(\w+)', re.IGNORECASE)
		self.pat2 = re.compile('(very|slightly|a little|not)?\s+(mad|angry|happy|calm|sad|afraid|worried|tired|bored|fine|joyful|disgruntled|dissastisfied|disturbed)', re.IGNORECASE)
		self.pat3 = re.compile('.*(to)?(/s)?(relax|wave|laugh|cry|talk|chat|walk|run|jump|hit|bow|pick|lick|fly|pushup|dance|fight|surf)', re.IGNORECASE)
		self.pat4 = re.compile('(\s)?(film|drama|comedy|action|movie|relationship|religion|science|joke|news|death|birth|job|hobb(y|i)?|trust|friend|friendship|food|car|technology|management|electric|computer|phone|celllular|biology|chemistry|sex|language|education|physics|train|airplane|music|television|tv|song|dream|dance|sport|etimolog(y|i)?)(s|es)?(/s)?', re.IGNORECASE)
		self.pat5 = re.compile('^my name is not', re.IGNORECASE)
		self.pathappy = re.compile('((peace|serene|play|nice|smart|friend|partner)|(happy|joy|sorry|please|funny|cheer|beautiful|cute|great)|(ecstatic|love|compassion))', re.IGNORECASE)
		self.patfear = re.compile('((danger|fear|punch|monster)|(hit|slap|kick|ghost|devil|scar|shut up)|(terr|blood|death|murder|kill|kidnap|bees))', re.IGNORECASE)
		self.patsad = re.compile('((ugly|hate|lie|leav)|(gone|miss|died|sad|ignore|not talking|get lost)|(death|ignore|disappoint))', re.IGNORECASE)
		self.patanger = re.compile('((kill|kick|war|enemy|shoot)|(stupid|angry|mad|punch|hit)|(rage|furious|cheat|lie|ugly|dummy|idiot))', re.IGNORECASE)

	def matchRule(self, inputstring):
		print "matching rule..."
		m1_out = None
		m2_out = [None,None]
		#m2_out2 = None
		m3_out = None
		m4_out = None
		m5_out = None
		happy_out = None
		fear_out = None
		sad_out = None
		anger_out = None
		m1 = self.pat1.match(inputstring)
		m2 = self.pat2.findall(inputstring)
		m3 = self.pat3.match(inputstring)
		m4 = self.pat4.search(inputstring)
		m5 = self.pat5.match(inputstring)
		mhappy = self.pathappy.findall(inputstring)
		mfear = self.patfear.findall(inputstring)
		msad = self.patsad.findall(inputstring)
		manger = self.patanger.findall(inputstring)
		emo=[None]

		if m1:
			if m1.group(2) is not 'am':
				#print "m1 match. verb:", m1.group(2)
				m1_out = m1.group(2)
				#print "m1 match. verb:", m1.group(3)
				#m1_out = m1.group(3)
		#else:
			#print "m1 does not match"

		if m2:
			#print "m2 match. emotion:", m2[0][3]
			m2_out = [m2[0][0], m2[0][1]]
			#m2_out2 = m2[0][4]
		#else:
			#print "m2 does not match"

		if m3:
			#print "m3 match. caught verb:", m3.group(1)
			#m3_out = m3.group(1)
			#print "m3 match. caught verb:", m3.group(3)
			m3_out = m3.group(3)
		#else:
			#print "m3 does not match"

		if m4:
			#print "m4 match. topic:", m4.group(2), m4.group(5)
			m4_out = m4.group(2)
		#else:
			#print "m4 does not match"
		
		if m5: 
			print "m5 match."
			m5_out = True
			
		if mhappy or mfear or msad or manger:
			print "mhappy or mfear or msad or manger match"
			#emo = [mhappy, mfear, msad, manger]
			#if mhappy is not None: mhappy=mhappy.groups()		
			#if mfear is not None: mfear=mfear.groups()
			#if msad is not None: msad=msad.groups()
			#if manger is not None: manger=manger.groups()
			emo = [mhappy, mfear, msad, manger]
			
		return m1_out, m2_out, m3_out, m4_out, m5_out, emo
	
	def filter(self,h):
		for i in h:
			if i is not '': return i
			
def main():
	lr = locoRegex()
	print lr.matchRule("shut up")

if __name__ == "__main__": main()
