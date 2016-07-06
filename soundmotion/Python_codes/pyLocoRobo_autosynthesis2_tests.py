from mosynth16_p import MotionSynthesizer
import resampling, math, numpy

ms = MotionSynthesizer()
resample = resampling.resample
fparam = {'motion': [], 'motionbuffer': [], 'interp': {'bias': 0, 'tension': 0, 'continuity': 0}, 'rate': 1, 'gains': [0,0,0], 'waveshapef': '', 'waveshapeg': [], 'awareness': {'orientation':"", 'position':"", 'target':""}}

fparam['gains'] = [2,0,0]
"""===readMotion(path):
    function: read .csv file from path
    input argument: path to .csv file (absolute)
    returns: motion in list format
    needs global variable(s): None
    affects global variable(s): None
"""
def readMotion(path):
    print "readMotion()...",
    try:        
        motion = ms.read(path)
        if motion:            
            print "motion:",path,"loaded."
            print motion
            return ms.read(path)
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
def setMotionbuffer(motion):
    print "setMotions()...",
    try:
        fparam['motionbuffer'].append(motion)
        if fparam['motionbuffer']:
            print "fparam['motionbuffer'] is set. Length:", len(fparam['motionbuffer'])
            print fparam['motionbuffer']
        else: print "fparam['motionbuffer'] is not set."
    except:
        print "error!"

def setMotion(motion):
    print "setMotion()...",
    try:        
        if motion:
            fparam['motion'] = motion
            print "fparam['motion'] is set. Length:", len(fparam['motion'])
            print fparam['motion']
        else: print "fparam['motion'] is not set."
    except:
        print "error!"

"""===clearMotion():
    function: clears the global variable fparam['motion']
    input argument: None
    returns: None
    needs global variable(s): None
    affects global variable(s): fparam['motion']
"""
def clearMotion():
    print "clearMotion()..."
    try:
        fparam['motion'] = []
        if len(fparam['motion']) == 0: print "cleared!"
        else: print "fparam['motion'] not empty."
    except:
        print "error!"

"""===clearMotions():
    function: clears the global variable fparam['motionbuffer']
    input argument: None
    returns: None
    needs global variable(s): None
    affects global variable(s): fparam['motionbuffer']
"""
def clearMotionbuffer():
    print "clearMotionbuffer()..."
    try:
        fparam['motionbuffer'] = []
        if len(fparam['motionbuffer']) == 0: print "cleared!"
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
def setInterpTension(value):
    print "Old Tension =", fparam['interp']['tension'],
    #interpTension = value
    fparam['interp']['tension'] = value
    print "new Tension =", fparam['interp']['tension']

"""===setInterpBias(value):
    function: set the value for global variable fparam['interp']['bias'] (bias parameter for function interpolate())
    input argument: value (int) for global variable fparam['interp']['bias']
    returns: None
    needs global variable(s): None
    affects global variable(s): fparam['interp']['bias']
"""
def setInterpBias( value):
    print "Old Bias =", fparam['interp']['bias'],
    #interpBias = value
    fparam['interp']['bias'] = value
    print "new Bias =", fparam['interp']['bias']

"""===setInterpContinuity(value):
    function: set the value for global variable fparam['interp']['continuity'] (continuity parameter for function interpolate())
    input argument: value (int) for global variable fparam['interp']['continuity']
    returns: None
    needs global variable(s): None
    affects global variable(s): fparam['interp']['continuity']
"""
def setInterpContinuity( value): 
    print "Old Continuity =", fparam['interp']['continuity'],
    #interpContinuity = value
    fparam['interp']['continuity'] = value
    print "new Continuity =", fparam['interp']['continuity']

def setRate(value):
    print "Old rate =", fparam['rate'],
    fparam['rate'] = value
    print "New rate =", fparam['rate']
#def loadMotion():
#    loadData(ui.comboBoxMotionSignal.currentText())

def setWaveshapef(expression):
    fparam['waveshapef'] = expression
    return 1

def setWaveshapeg(waveshap):
    fparam['waveshapeg'] = waveshap
    
"""===interpolate(motion):
    function: interpolate a single motion
    input argument: motion (2-D array/list) to be interpolated
    returns: interpolated motion
    needs global variable(s): fparam['motion'], fparam['interp']['bias', 'tension', 'continuity']
    affects global variable(s): None
"""
def interpolate(motion):
    print "interpolate()...",
    try:
        print "fparam['motion']:", fparam['motion']
        print "fparam['interp']['bias']:", fparam['interp']['bias'], "; fparam['interp']['tension']:", fparam['interp']['tension'], "; fparam['interp']['continuity']:", fparam['interp']['continuity']

        #interpolatedmotion = [ms.interpolate(m, fparam['interp']['bias'], fparam['interp']['tension'], fparam['interp']['continuity']) for m in fparam['motion']]
        interpolatedmotion = ms.interpolate(motion, fparam['interp']['bias'], fparam['interp']['tension'], fparam['interp']['continuity'])
        return interpolatedmotion
    except:
        print "error!"

"""===interpolateAllMotions():
    function: interpolate each motion in fparam['motion'] separately.
        For example: if there are 3 motions in fparam['motion'], the result will be three interpolated motions in fparam['motion']
    input argument: None
    returns: None
    needs global variable(s): fparam['motionbuffer']
    affects global variable(s): fparam['motion']
"""
def interpolateAllMotions():
    print "interpolateAllMotions()..."
    tmp = [interpolate(m) for m in fparam['motion']]
    fparam['motion'] = tmp
    print "len(fparam['motion'])=", len(fparam['motion']), "fparam['motion']:", fparam['motion']

"""===resampleData2():
    function: exterpolate motion data (i.e. resample - makes the motion faster)
    input argument: None
    returns: None
    needs global variable(s): fparams['rate'], motion data (tentatively: fparam['motion'])
    affects global variable(s): current motion data (tentatively: fprarm['motion'])
"""
def resampleData2():
    resample = resampling.resample
    #rate = ui.rateSpinBox.value()
    ui.rateSpinBox.setValue(fparams['rate'])
    new_data = []
    for data in ms.DATA:
        new_data.append(resample(data, rate))
    ms.multiresFiltering(new_data)
    #updatePlot()
    print "autosampling..."

"""===resample(motion):
    function: extrapolate motion data
    input argument: one motion data
    returns: extrapolated motion data
    needs global var(s):
    affects global var(s):
"""
def resamplez(motion):
    print "resample()..."
    try:        
        tmp = [resample(data, fparam['rate']) for data in motion]
        if tmp:
            print "resampling successful."
            print "tmp =", tmp
            return tmp
        else: print "resampling failed."
    except:
        print "error!"

def resampling():
    return [resamplez(motion) for motion in fparam['motion']]

def resamplingAll():
    return [resamplez(motion) for motion in fparam['motionbuffer']]

"""===modifyGains():
    function: modify motion data by adjusting the gain values
    input argument: None
    returns: None
    needs global variable(s): fparam['gains']
    affects global variable(s): None
"""
def modifyGains():
    #n = len(ms.countGains())
    n = 9                       # static for test purposes...
    [start, step] = defstep(n)
    indices = range(start, n, step)
    for i in range(0,3):
        #setSliderValue(fparam['gains'][i], indices[i])
        print "fparam['gains'][", i, "]=", fparam['gains'][i], "; indices[", i,"]=", indices[i]



"""===defstep(x):
    function: given x number of gains, find the low, medium, high gain indices
    input argument: x (i.e. number of gains)
    returns: initial index, steps
    needs global variable(s): None
    affects global variable(s): None
"""
def defstep( x):
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
def concatMotion():
    print "concatMotion()...",
    try:
        if len(fparam['motionbuffer']) >= 2:
            concatenated = reduce(lambda m1, m2: ms.concatenatemotion(m1,m2), fparam['motionbuffer'])
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
            
"""===superpose():
    function: combine/blend two motions into one (currently can't be done properly when the lengths of the two motions are different)
    input arguments: motion1 and motion2 -- the two motions to be combined
    returns: None
    needs global variable(s): None
    affects global variable(s): None (if working, current motion)
"""
def superpose(motion1, motion2):
    try:
        tmp = []
        #data = ms.returnNewData()
        print "Superpose!"

        for i in range(len(motion1)):
            try:
                tmpData = list(numpy.add(motion1[i], numpy.multiply(motion2[i], 0.5)))
                ui.statusbar.showMessage("Superposing...")                    
            except:
                #print "length data: ", len(data[i]), "points = ", len(new_points)
                ui.statusbar.showMessage("Waveshape 2 failed.")
            tmp.append(tmpData)
            ui.qwtPlot.changeCurve(i, tmpData)

        #newData = tmp
        ms.DATA = tmp
            
    except:
        ui.statusbar.showMessage("Uh oh, something is wrong...")

"""===waveshapef():
    function: creates a waveshaping waveform using a function in fparam['waveshapef']
    input arguments: None
    returns: None
    needs global variable(s): fparam['waveshapef']
    affects global variable(s): Currently none (should be: fparam['motion'])
"""
def waveshapef():
    try:
        text = unicode(fparam['waveshapef'])
        #x = 2
        ui.statusbar.showMessage("Auto-Waveshaping function(x) = %s" % (text))
        c = 0
        y = []

        currentData = ms.returnNewData()
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

def waveshapeftest():
    print "waveshapeftest...",
    try:
        print "ok."
        for x in range(10):
            print eval(fparam['waveshapef'])
    except:
        print "meh."

"""===applyWaveshapef():
    function: applying waveshaping function from waveshapef() to motion data
    input arguments: None
    returns: None
    needs global variable(s): None
    affects global variable(s): Currently none (should be: fparam['motion'])
"""
def applyWaveshapef():
    multiplier = 0.15
    try:
        tmp = []
        data = ms.returnNewData()

        for i in range(len(data)):
            tmpData = list(numpy.add(data[i], numpy.multiply(data[i], numpy.multiply(y, multiplier))))
            tmp.append(tmpData)
            ui.qwtPlot.changeCurve(i, tmpData)

        #newData = tmp
        ms.DATA = tmp
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
def waveshapeg():  # derived from pointChange(...)
    try:
        print "Applying waveshapeg"
        
        for p in fparam['waveshapeg']:
            points[p[0]] = p[1] * 0.1
        #print "value in point ", currentPointIndex, "= ", points[currentPointIndex]
        print "points = ", points
        new_points = ms.interpolate2(points)
        #print "interpolated points: ", new_points
        plotWave(ui.wavePlot, range(len(new_points)), new_points)
    except:
        print "Waveshapeg failed..."

def waveshapegtest():
    print "waveshapeg...",
    try:
        print "ok."
        points = numpy.zeros(10)
        for p in fparam['waveshapeg']:
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

def awareness():
    pass


ffunct = {'interpolate':interpolate, 'resample':resampleData2, 'modifygains':modifyGains, 'blend':concatMotion, 'waveshapefunct': waveshapef, 'waveshapegraph': waveshapeg}
ffunctlist = [interpolate, interpolateAllMotions, resampling, resamplingAll, modifyGains, waveshapeftest, waveshapegtest, concatMotion, awareness]

###=========================TESTS=====================================================

if __name__ == "__main__":
    mpath1 = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH1.csv"
    mpath2 = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH2.csv"
    mpath3 = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH3.csv"

    setMotionbuffer(readMotion(mpath1))
    setMotionbuffer(readMotion(mpath2))

    #setMotion([concatMotion()])
    #ffunctlist[1]()
    #concatMotion()
    setRate(2)
    #resampling()
    setWaveshapef('math.pow(2*x, 2)')
    setWaveshapeg([[0,2],[2,7],[5,6]])

    
    order = [7,1,2,5,6]

    for m in order:
        ffunctlist[m]()

    #flist = [ffunctlist[i] for i in order]
    #print flist

    #reduce(lambda x,y: y([x]), flist)
    #for f in flist:
    #    f()

    

"""    #test readMotion()
    loadedmotion = readMotion(mpath1)   #<< pass
    if loadedmotion:
        print "motion ready."

    print "======================================================================================================================="

    #test setMotion()
    setMotions(loadedmotion) #<< pass

    print "======================================================================================================================="
    
    #test appending multiple motion to fparam['motion']
    setMotions(readMotion(mpath2))   #<< pass
    #setMotion(readMotion(mpath3))   #<< pass
    print "======================================================================================================================="
    #test clearMotion()
    #clearMotion()  #<< pass
    print "======================================================================================================================="
    #test setInterpBias(value)
    setInterpBias(2)    #<< pass
    print "======================================================================================================================="
    #test setInterpTension(value)
    setInterpTension(3) #<< pass
    print "======================================================================================================================="
    #test setInterpContinuity(value)
    setInterpContinuity(2)  #<< pass
    print "======================================================================================================================="
    #test interpolate()
    #interpolate()   #<< failed -- fparam['motion'] is a 3 dimensional array/list.  ms.interpolate only deals with 2-d array/list.  must iterate inside fparam['motion'], or motions must be concatenated first
    #interpolate() #<< pass -- iterate inside fparam['motion'] to INTERPOLATE EACH MOTION in fparam['motion']
    # --------------------------- note: don't iterate inside interpolate() >> let the interpolation done for one motion at a time
    #interpolateAllMotions()    

    #test concatMotion()
    print "======================================================================================================================="    
    temp = concatMotion()   #<< pass
    setMotion([temp])
    interpolateAllMotions()
    #inter"""
"""if temp:
        clearMotion()
        #setMotion()     #<< concatenated motion replaces all the motions in the fparam['motion'] (len = 1) -- check if this is a desired effect
        interpolateAllMotions()"""
"""print "======================================================================================================================="
    setRate(3)

    #print "fparam['motion'][0]=", fparam['motion'][0]
    #resample(fparam['motion'][0])   #<< pass - partially (these functions should have no arguments ... maybe)
    print "======================================================================================================================="

    modifyGains()   #<< pass
    print "======================================================================================================================="
    print "motion buffer:", fparam['motionbuffer']
    print "motion:", fparam['motion'][0][0]
"""
#fparam = {'motion': [], 'motionbuffer': [], 'interp': {'bias': 0, 'tension': 0, 'continuity': 0}, 'rate': 1,
#    'gains': [], 'waveshapef': '', 'waveshapeg': [], 'awareness': {'orientation':"", 'position':"", 'target':""}}


class params:
    def __init__(self, motion=[], motionbuffer=[], bias=0, tension=0, continuity=0, rate=1, lgain=0, mgain=0, hgain=0, waveshapef=None, waveshapeg=[], orientation=None, position=None, target=None ):
        self.motion = motion
        self.motionbuffer = motionbuffer
        self.interp = {'bias': bias, 'tension': tension, 'continuity': continuity}
        self.rate = 1
        self.gains = {'lgain': lgain, 'mgain': mgain, 'hgain': hgain}
        self.waveshapef = waveshapef
        self.waveshapeg = waveshapeg
        self.awareness = {'orientation': orientation, 'position': position, 'target': target}

    def setMotionBuffer(self, motionlist):
        self.motionbuffer = motionlist

    def addToMotionBuffer(self, motion):
        self.motionbuffer.append(motion)

    def getMotionBuffer(self):
        return self.motionbuffer

    def setInterpBias(self, value):
        self.interp['bias'] = value

    def setInterpTension(self, value):
        self.interp['tension'] = value

    def setInterpContinuity(self, value):
        self.interp['continuity'] = value

    def getInterpBias(self):
        return self.interp['bias']

    def getInterpTension(self):
        return self.interp['tension']

    def getInterpContinuity(self):
        return self.interp['continuity']

    def getInterp(self, d=False):
        if d: return self.interp
        else: return self.interp['bias'], self.interp['tension'], self.interp['continuity']

    def setRate(self, value):
        self.rate = value

    def getRate(self, value):
        return self.rate

    def setGainsL(self, value):
        self.gains['lgain'] = value

    def setGainsM(self, value):
        self.gains['mgain'] = value

    def setGainsH(self, value):
        self.gains['lgain'] = value

    def setGains(self, gains):
        if len(gains) == 3:
            self.gains['hgain'] = gains[0]
            self.gains['mgain'] = gains[1]
            self.gains['lgain'] = gains[2]
        else:
            print "Please provide a list of 3 freq gain values in order: [high_freq_gain, med_freq_gain, low_freq_gain]"
            return 0

    def setWaveshapef(self, function):
        self.waveshapef = str(function)

    def getWaveshapef(self):
        if self.waveshapef is not "":
            return self.waveshapef
        else:
            print "The waveshaping function is not yet defined"
            return 0

    def setWaveshapeg(self, form):
        self.waveshapeg = form

    def getWaveshapeg(self, form):
        return self.waveshapeg

    def getAll(self):
        return {'motion': self.motion, 'motionbuffer': self.motionbuffer, 'interp': {'bias': self.interp['bias'], 'tension': self.interp['tension'], 'continuity': self.interp['continuity']}, 'rate': self.rate, 'gains': self.gains, 'waveshapef': self.waveshapef, 'waveshapeg': self.waveshapeg}

p = params()
print p.getAll()   
