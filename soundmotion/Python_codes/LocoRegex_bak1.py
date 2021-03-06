import re

class locoRegex:

    def __init__(self):
        #self.pat1 = re.compile('(\S+\s+)*I\s+(\w+)', re.IGNORECASE)
        self.pat1 = re.compile('(\S+\s+)*I\s+^(like|feel|can|have|will|should|would|could|did|do|seem|suppose)*\s+(\w+)', re.IGNORECASE)
        self.pat2 = re.compile('(\S+\s+)*(i(\s+am|\'m)* (mad|angry|happy|calm|sad|afraid|worried|tired|bored|fine|joyful|disgruntled|dissastisfied|disturbed))', re.IGNORECASE)
        self.pat3 = re.compile('.*(to)?(/s)?(relax|laugh|cry|talk|chat|walk|run|jump|hit|bow|pick|lick|fly|pushup|dance|fight)', re.IGNORECASE)
        self.pat4 = re.compile('(\s)?(film|drama|comedy|action|movie|relationship|religion|science|joke|news|death|birth|job|hobb(y|i)?|trust|friend|friendship|food|car|technology|management|electric|computer|phone|celllular|biology|chemistry|sex|language|education|physics|train|airplane|music|television|tv|song|dream|dance|sport|etimolog(y|i)?)(s|es)?(/s)?', re.IGNORECASE)

    def matchRule(self, inputstring):
        m1_out = None
        m2_out = None
        m3_out = None
        m4_out = None
        m1 = self.pat1.match(inputstring)
        m2 = self.pat2.findall(inputstring)
        m3 = self.pat3.match(inputstring)
        m4 = self.pat4.search(inputstring)

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
            m2_out = m2[0][3]
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
            

        return m1_out, m2_out, m3_out, m4_out
    
            
