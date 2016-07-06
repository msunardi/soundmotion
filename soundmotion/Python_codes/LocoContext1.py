from LocoRegex import locoRegex

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
        #self.mov = autoSynthesis()
        self.motionFilePath = ["/home/msunardi/Documents/thesis-stuff/KHR-1-motions/push_ups_data.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_bird.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_left.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backflip.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/backward_roll.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/dance2.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/flying.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/goodwalk.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/home.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/karatekid.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_angry.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_cocky.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_relax.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_surprised.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/posture_tired.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/pulsing.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/pulsing2.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/pulsing3.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/wave_right_arm.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/weirdarmgesture.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/weirdarmgesture2.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_swing_leftright.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_bird.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_left.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/sweetescape_surf_right.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/cartwheel.csv",
                               "/home/msunardi/Documents/thesis-stuff/KHR-1-motions/Extrm_CH1.csv"]  # <<< Selected motion signals
        
        self.lr = locoRegex()

    def lcKeywords(self, inputstring):
        (self.miscverb, self.emotion, self.keyverb) = self.lr.matchRule(inputstring)
        print "miscverb:", self.miscverb, ", emotion:", self.emotion, ", keyverb:", self.keyverb
        return 1

    def updateContext(self):
        if self.miscverb is not None: #== self.keyverb:
            update = True
            if self.keyverb == 'relax':
                pass
                #invoke (push to motionbuffer) relax pose
            elif self.keyverb == 'walk':
                pass
                #invoke walk action
            elif self.keyverb == 'dance':
                pass
                #invoke dance action
            elif self.keyverb == 'fly':
                pass
                #invoke fly action

            if self.emotion == 'mad' or self.emotion == 'angry':
                print "mad / angry: set angry pose, sampling rate=3, gain++, interp tension++"
                #set angry pose
                #set (sampling) rate = 3
                #set gain ++ (higher)
                #set interp tension ++ (higher)
            elif self.emotion == 'happy' or self.emotion == 'joyful':
                print "happy / joyful: set sampling rate=3, gain++, interp continuity++, tension--"
                #set (sampling) rate = 3
                #set gain ++
                #set interp continuity ++, tension -- (less)
            elif self.emotion == 'sad' or self.emotion == 'tired' or self.emotion == 'bored':
                print "sad / tired / bored: set tired pose, gain--"
                #set tired pose
                #set gain --
            else:
                update = False
                print "update", update
        else:
            update = False
            print "update", update
        return update

    def getMotionResponse(self):
        print "getMotionResponse()"    #Test
        #process/apply everything (just pick an order)
        #return self.mov['motion']

#======================
# Test LocoContext
#======================

lc = locoContext()
lc.lcKeywords("i run and i'm tired")
#lc.getMotionResponse()
lc.updateContext()

#======================
# from pyLocoRobo_autoshynthesis2
#======================
class autoSynthesis:
    def __init__(self):
        from mosynth16_p import MotionSynthesizer
        import resampling, math, numpy
        
        self.ffunct = {'interpolate':self.interpolate, 'resample':self.resampleData2, 'modifygains':self.modifyGains, 'blend':self.concatMotion, 'waveshapefunct': self.waveshapef, 'waveshapegraph': self.waveshapeg}
        self.ffunctlist = [self.interpolate, self.interpolateAllMotions, self.resampling, self.resamplingAll, self.modifyGains, self.waveshapeftest, self.waveshapegtest, self.concatMotion, self.awareness]
        self.ms = MotionSynthesizer()
        self.resample = resampling.resample
        self.fparam = {'motion': [],
                       'motionbuffer': [],
                       'interp': {'bias': 0, 'tension': 0, 'continuity': 0},
                       'rate': 1,
                       'gains': [0,0,0],
                       'waveshapef': '',
                       'waveshapeg': [],
                       'awareness': {'orientation':"", 'position':"", 'target':""}}
        pass

    """===readMotion(path):
        function: read .csv file from path
        input argument: path to .csv file (absolute)
        returns: motion in list format
        needs global variable(s): None
        affects global variable(s): None
    """
    def readMotion(self, path):
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
    def setMotionbuffer(self, motion):
        print "setMotions()...",
        try:
            self.fparam['motionbuffer'].append(motion)
            if self.fparam['motionbuffer']:
                print "fparam['motionbuffer'] is set. Length:", len(self.fparam['motionbuffer'])
                print self.fparam['motionbuffer']
            else: print "fparam['motionbuffer'] is not set."
        except:
            print "error!"

    def setMotion(self, motion):
        print "setMotion()...",
        try:        
            if motion:
                self.fparam['motion'] = motion
                print "fparam['motion'] is set. Length:", len(self.fparam['motion'])
                print self.fparam['motion']
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
    def clearMotion(self):
        print "clearMotion()..."
        try:
            self.fparam['motion'] = []
            if len(self.fparam['motion']) == 0: print "cleared!"
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
        print "Old Tension =", self.fparam['interp']['tension'],
        #interpTension = value
        self.fparam['interp']['tension'] = value
        print "new Tension =", self.fparam['interp']['tension']

    """===setInterpBias(value):
        function: set the value for global variable fparam['interp']['bias'] (bias parameter for function interpolate())
        input argument: value (int) for global variable fparam['interp']['bias']
        returns: None
        needs global variable(s): None
        affects global variable(s): fparam['interp']['bias']
    """
    def setInterpBias(self, value):
        print "Old Bias =", self.fparam['interp']['bias'],
        #interpBias = value
        self.fparam['interp']['bias'] = value
        print "new Bias =", self.fparam['interp']['bias']

    """===setInterpContinuity(value):
        function: set the value for global variable fparam['interp']['continuity'] (continuity parameter for function interpolate())
        input argument: value (int) for global variable fparam['interp']['continuity']
        returns: None
        needs global variable(s): None
        affects global variable(s): fparam['interp']['continuity']
    """
    def setInterpContinuity(self, value): 
        print "Old Continuity =", self.fparam['interp']['continuity'],
        #interpContinuity = value
        self.fparam['interp']['continuity'] = value
        print "new Continuity =", self.fparam['interp']['continuity']

    def setRate(self, value):
        print "Old rate =", self.fparam['rate'],
        self.fparam['rate'] = value
        print "New rate =", self.fparam['rate']
    #def loadMotion():
    #    loadData(ui.comboBoxMotionSignal.currentText())

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
    def interpolate(self, motion):
        print "interpolate()...",
        try:
            print "fparam['motion']:", self.fparam['motion']
            print "fparam['interp']['bias']:", self.fparam['interp']['bias'], "; fparam['interp']['tension']:", self.fparam['interp']['tension'], "; fparam['interp']['continuity']:", self.fparam['interp']['continuity']

            #interpolatedmotion = [ms.interpolate(m, fparam['interp']['bias'], fparam['interp']['tension'], fparam['interp']['continuity']) for m in fparam['motion']]
            interpolatedmotion = ms.interpolate(motion, self.fparam['interp']['bias'], self.fparam['interp']['tension'], self.fparam['interp']['continuity'])
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
    def interpolateAllMotions(self):
        print "interpolateAllMotions()..."
        tmp = [interpolate(m) for m in self.fparam['motion']]
        self.fparam['motion'] = tmp
        print "len(self.fparam['motion'])=", len(self.fparam['motion']), "fparam['motion']:", self.fparam['motion']

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
    def resamplez(self, motion):
        print "resample()..."
        try:        
            tmp = [resample(data, self.fparam['rate']) for data in motion]
            if tmp:
                print "resampling successful."
                print "tmp =", tmp
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
        #n = len(ms.countGains())
        n = 9                       # static for test purposes...
        [start, step] = defstep(n)
        indices = range(start, n, step)
        for i in range(0,3):
            #setSliderValue(fparam['gains'][i], indices[i])
            print "fparam['gains'][", i, "]=", self.fparam['gains'][i], "; indices[", i,"]=", indices[i]



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
                concatenated = reduce(lambda m1, m2: ms.concatenatemotion(m1,m2), self.fparam['motionbuffer'])
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
    def superpose(self, motion1, motion2):
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
    def waveshapef(self):
        try:
            text = unicode(self.fparam['waveshapef'])
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
    def waveshapeg(self):  # derived from pointChange(...)
        try:
            print "Applying waveshapeg"
            
            for p in self.fparam['waveshapeg']:
                points[p[0]] = p[1] * 0.1
            #print "value in point ", currentPointIndex, "= ", points[currentPointIndex]
            print "points = ", points
            new_points = ms.interpolate2(points)
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


    
