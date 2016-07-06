import re,sys

pat0 = re.compile('exit[()]')
pat1 = re.compile('\d+')
pat2 = re.compile('(\w+\s+)*fall')
pat3 = re.compile('(\S+\s+)*I\s+(\w+)', re.IGNORECASE)
pat4 = re.compile('(\S+\s+)*(i(\s+am|\'m) (mad|angry|happy|sad|afraid|worried|tired|bored|fine|joyful|disgruntled|dissastisfied|disturbed))', re.IGNORECASE)
pat5 = re.compile('.*(relax|laugh|cry|talk|walk|run|jump|hit|bow|pick|lick)')

#pat5 = re.compile('^|\s*\w*|\w*\s*|\W*(i(\s+am|\'m)+ (mad|angry|happy|sad|afraid|worried|tired|bored)+)+\w*', re.IGNORECASE)
#pat5 = re.compile('(i((?:\s+am)|(?:\'m))\s(mad))\w*', re.IGNORECASE)
pat6 = re.compile('(\s)?(movie|relationship|religion|science|joke|news|death|birth|job|hobb(y|i)?|trust|friend|friendship|food|car|technology|management|electric|computer|phone|celllular|biology|chemistry|sex|language|education|physics|train|airplane|music|television|tv|song|dream|dance|sport|etimolog(y|i)?)(s|es)?(/s)?')

j = {'param1': 0, 'param2': 0, 'param3': 0}

def matchRule(inputstring):
    m1 = pat1.match(inputstring)
    m2 = pat2.match(inputstring)
    m3 = pat3.match(inputstring)
#    m4 = pat5.match(inputstring)
    m4 = pat4.findall(inputstring)
    m5 = pat5.match(inputstring)
    m6 = pat6.search(inputstring)
    
    #if pat2.match(inputstring):
#    if m1:
#        print 'pat2 match:'
#        iterati = pat2.finditer(inputstring)
#        fall = pat2.findall(inputstring)
#        for i in iterati:
#            print i.group()
#        #print "fall 0:", fall[0]
#    #if pat3.match(inputstring):
    if m2:
#        fall = pat3.findall(inputstring)
#        print 'pat3 match:', fall
        print 'pat2 match:', m2.group()
    #if pat4.match(inputstring):
    if m3:
        #fall = pat4.match(inputstring)
        fall = m3
        #print 'pat3 match:', fall.group(0)
        print 'pat4 match:', fall.groups(), 'keywords:', fall.group(1), fall.group(2)
    #if pat5.match(inputstring):
#    if m4:
    if len(m4) > 0:
        #fall = pat5.match(inputstring)
        fall = m4
#        print 'pat4 match:', fall.group()
#        f = pat5.findall(inputstring)
#        print f[0][3], type(f[0][3])
        print 'pat4 match:', m4[0][3], type(m4[0][3])

    if m5:
        print 'pat5 match:', m5.group(1)

    if m6:
        print 'pat6 match:', m6.group(2), m6.group(5)

#=================MAIN LOOP
while True:
    ans = raw_input('say> ')
    if pat1.match(ans):
        print "Goodbye"
        sys.exit()
    else:
        matchRule(ans)
        
