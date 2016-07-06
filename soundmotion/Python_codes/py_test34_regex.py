import re,sys

pat1 = re.compile('exit[()]')
pat2 = re.compile('\d+')
pat3 = re.compile('(\w+\s+)*fall')
pat4 = re.compile('(\S+\s+)*I\s+(\w+)', re.IGNORECASE)
pat5 = re.compile('(\S+\s+)*(i(\s+am|\'m) (mad|angry|happy|sad|afraid|worried|tired|bored))', re.IGNORECASE)
pat6 = re.compile('.*(relax|laugh|cry|talk|walk|run|jump|hit|bow|pick|lick)')
#pat5 = re.compile('^|\s*\w*|\w*\s*|\W*(i(\s+am|\'m)+ (mad|angry|happy|sad|afraid|worried|tired|bored)+)+\w*', re.IGNORECASE)
#pat5 = re.compile('(i((?:\s+am)|(?:\'m))\s(mad))\w*', re.IGNORECASE)

j = {'param1': 0, 'param2': 0, 'param3': 0}

def matchRule(inputstring):
    m1 = pat2.match(inputstring)
    m2 = pat3.match(inputstring)
    m3 = pat4.match(inputstring)
#    m4 = pat5.match(inputstring)
    m4 = pat5.findall(inputstring)
    m5 = pat6.match(inputstring)
    
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
        print 'pat3 match:', m2.group()
    #if pat4.match(inputstring):
    if m3:
        #fall = pat4.match(inputstring)
        fall = m3
        #print 'pat4 match:', fall.group(0)
        print 'pat4 match:', fall.groups(), 'keywords:', fall.group(1), fall.group(2)
    #if pat5.match(inputstring):
#    if m4:
    if len(m4) > 0:
        #fall = pat5.match(inputstring)
        fall = m4
#        print 'pat5 match:', fall.group()
#        f = pat5.findall(inputstring)
#        print f[0][3], type(f[0][3])
        print 'pat5 match:', m4[0][3], type(m4[0][3])

    if m5:
        print 'pat6 match:', m5.group(1)

#=================MAIN LOOP
while True:
    ans = raw_input('say> ')
    if pat1.match(ans):
        print "Goodbye"
        sys.exit()
    else:
        matchRule(ans)
        
