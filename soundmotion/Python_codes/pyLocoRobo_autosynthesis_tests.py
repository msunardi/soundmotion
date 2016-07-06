from mosynth15_p import MotionSynthesizer
import resampling

ms = MotionSynthesizer()
fparam = {'motion': [], 'motions': [], 'interp': {'bias': 0, 'tension': 0, 'continuity': 0}, 'rate': 1, 'gains': [], 'waveshapef': '', 'waveshapeg': [], 'awareness': {'orientation':"", 'position':"", 'target':""}}

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

"""===setMotion(motion):
    function: store loaded motion to global variable fparam['motions']
    input argument: motion in list form (normally from/output of readMotion())
    returns: None
    needs global variable(s): None
    affects global variable(s): fparam['motions']
"""
def setMotions(motion):
    print "setMotions()...",
    try:
        fparam['motions'].append(motion)
        if fparam['motions']:
            print "fparam['motions'] is set. Length:", len(fparam['motions'])
            print fparam['motions']
        else: print "fparam['motions'] is not set."
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
    function: clears the global variable fparam['motions']
    input argument: None
    returns: None
    needs global variable(s): None
    affects global variable(s): fparam['motions']
"""
def clearMotions():
    print "clearMotions()..."
    try:
        fparam['motions'] = []
        if len(fparam['motions']) == 0: print "cleared!"
        else: print "fparam['motions'] not empty."
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
        """for m in fparam['motion']:
            interpolateddata = ms.interpolate(m, fparam['interp']['bias'], fparam['interp']['tension'], fparam['interp']['continuity'])
            if interpolateddata:
                #return ms.interpolate(fparam['motion'], fparam['interp']['bias'], fparam['interp']['tension'], fparam['interp']['continuity'])
                print "data successfully interpolated."
                print "interpolateddata:", interpolateddata
                m = interpolateddata                
        
            else:
                print "interpolation failed."
            print fparam['motion']    
            return interpolateddata"""
        
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
    needs global variable(s): fparam['motions']
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
def resample(motion):
    print "resample()..."
    try:
        resample = resampling.resample
        tmp = [resample(data, fparam['rate']) for data in motion]
        if tmp:
            print "resampling successful."
            print "tmp =", tmp
            return tmp
        else: print "resampling failed."
    except:
        print "error!"

def resampling():
    return [resample(motion) for motion in fparam['motion']]

def resamplingAll():
    return [resample(motion) for motion in fparam['motions']]

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
        setSliderValue(fparam['gains'][i], indices[i])



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
    function: combine two motions sequentially into one
    input argument: None
    returns: concatenated (combined) motion
    needs global variable(s): fparam['motion']
    affects global variable(s): None
"""
def concatMotion():
    print "concatMotion()...",
    try:
        if len(fparam['motions']) >= 2:
            concatenated = reduce(lambda m1, m2: ms.concatenatemotion(m1,m2), fparam['motions'])
            if concatenated:
                print "motions concatenated."
                print "concatenated motion:", concatenated
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
def superpose( motion1, motion2):
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
        #print "points = ", points
        new_points = ms.interpolate2(points)
        #print "interpolated points: ", new_points
        plotWave(ui.wavePlot, range(len(new_points)), new_points)
    except:
        print "Waveshapeg failed..."
 
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
ffunctlist = [interpolate, resampleData2, modifyGains, waveshapef, waveshapeg, concatMotion, awareness]

###=========================TESTS=====================================================

if __name__ == "__main__":
    mpath1 = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH1.csv"
    mpath2 = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH2.csv"
    mpath3 = "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH3.csv"

    #test readMotion()
    loadedmotion = readMotion(mpath1)   #<< pass
    if loadedmotion:
        print "motion ready."

    #test setMotion()
    setMotions(loadedmotion) #<< pass

    #test appending multiple motion to fparam['motion']
    setMotions(readMotion(mpath2))   #<< pass
    #setMotion(readMotion(mpath3))   #<< pass

    #test clearMotion()
    #clearMotion()  #<< pass

    #test setInterpBias(value)
    setInterpBias(2)    #<< pass

    #test setInterpTension(value)
    setInterpTension(3) #<< pass

    #test setInterpContinuity(value)
    setInterpContinuity(2)  #<< pass

    #test interpolate()
    #interpolate()   #<< failed -- fparam['motion'] is a 3 dimensional array/list.  ms.interpolate only deals with 2-d array/list.  must iterate inside fparam['motion'], or motions must be concatenated first
    #interpolate() #<< pass -- iterate inside fparam['motion'] to INTERPOLATE EACH MOTION in fparam['motion']
    # --------------------------- note: don't iterate inside interpolate() >> let the interpolation done for one motion at a time
    #interpolateAllMotions()    

    #test concatMotion()
    
    temp = concatMotion()   #<< pass
    setMotion([temp])
    interpolateAllMotions()
    #inter
    """if temp:
        clearMotion()
        #setMotion()     #<< concatenated motion replaces all the motions in the fparam['motion'] (len = 1) -- check if this is a desired effect
        interpolateAllMotions()"""

    setRate(3)
    #print "fparam['motion'][0]=", fparam['motion'][0]
    resample(fparam['motion'][0])   #<< pass - partially (these functions should have no arguments ... maybe)

    modifyGains()   #<< pass

    

    
