from LocoRegex import locoRegex


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
        #self.fparam = {'motion': [],
        #               'pose': [],
        #               'motionbuffer': [],
        #               'interp': {'bias': 0, 'tension': 0, 'continuity': 0},
        #               'rate': 1,
        #               'gains': [0,0,0],
        #               'waveshapef': '',
        #               'waveshapeg': [],
        #               'awareness': {'orientation':"", 'position':"", 'target':""}}
        self.fparam = {'motionbuffer': [],
                       'pose': [],
                       'interpbias': [],
                       'interptension': [],
                       'interpcontinuity': [],
                       'rate': [],
                       'gains': [],
                       'gainslow': [],
                       'gainsmed': [],
                       'gainshigh': [],
                       'fftlow': [],                       
                       'ffthigh': [],
                       'waveshapef': [],
                       'waveshapeg': []}
        self.outputmotion = []
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
                print motion
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
                print self.fparam['motionbuffer']
            else: print "fparam['motionbuffer'] is not set."
        except:
            print "error!"
            return 0

    def countMotionbuffer(self):
        count = len(self.fparam['motionbuffer'])
        print "In Motionbuffer, there are", count, "motions."
        return count

    def getMotionbuffer(self):
        print "Retrieving Motionbuffer...", self.fparam['motionbuffer']
        return self.fparam['motionbuffer']

    def setPose(self, motion):
        print "setPose()...",
        try:
            self.fparam['pose'].append(motion)
            if self.fparam['pose']:
                print "fparam['pose'] is set. Length:", len(self.fparam['pose'])
                print self.fparam['pose']
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
                    self.fparam['gains'].append(self.ms.multiresFiltering(data))
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

    def getFparam(self, key, index=None):
        #if index in ['interpbias', 'interptension', 'interpcontinuity','rate','gainslow', 'gainsmed', 'gainshigh']:
        try:
            if index is not None:
                print "Current",key,index,":", self.fparam[key][index]
                return self.fparam[key][index]
            elif index is None:
                print "Current",key,"content:", self.fparam[key]
                return self.fparam[key]
            #if index is 'interp':
            #    print sub_index,":", self.fparam[index][sub_index]
            #    return self.fparam[index][sub_index]
            #else:
            #    print ":", self.fparam[index]
            #    return self.fparam[index]
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
    def interpolate(self, index):
        print "interpolate()...",
        try:
            motion = self.fparam['motionbuffer'][index]
            print "motionbuffer",index,":", motion
            print "bias:", self.fparam['interpbias'], "; tension:", self.fparam['interptension'], "; continuity:", self.fparam['interpcontinuity']

            #interpolatedmotion = [ms.interpolate(m, fparam['interp']['bias'], fparam['interp']['tension'], fparam['interp']['continuity']) for m in fparam['motion']]
            interpolatedmotion = self.ms.interpolate(motion, self.fparam['interpbias'], self.fparam['interptension'], self.fparam['interpcontinuity'])
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
            print "len(self.fparam['motion'])=", len(self.fparam['motion']), "fparam['motion']:", self.fparam['motion']
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
        n = len(self.ms.countGains())
        #n = 9                       # static for test purposes...
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
        n = len(gains[0])
        gainadjustments = [gainslow, gainsmed, gainshigh]
        [start, step] = self.defstep(n)
        indices = range(start, n, step)
        for i in range(0,3):
            for channel in range(len(data)):
                self.ms.adjustGain(channel, indices, gainadjustments[i])
                
        return 

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
            self.ms.DATA = tmp
                
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
                       'gainslow': [],
                       'gainsmed': [],
                       'gainshigh': [],
                       'fftlow': [],                       
                       'ffthigh': [],
                       'waveshapef': [],
                       'waveshapeg': []}
        return 1
            

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

    def lcKeywords(self, inputstring):
        (self.miscverb, self.emotion, self.keyverb) = self.lr.matchRule(inputstring)
        print "miscverb:", self.miscverb, ", emotion:", self.emotion, ", keyverb:", self.keyverb
        return 1

    def updateContext(self):
        update = False
        if self.keyverb is not None or self.emotion is not None or self.miscverb is not None:
            update = True
            print "Context update...",
            if self.keyverb == 'relax':
                #invoke (push to pose) relax pose
                self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_relax']))
                
            elif self.keyverb == 'walk':
                #invoke (push to motionbuffer) walk action
                self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['walk']))
                
            elif self.keyverb == 'dance':                
                #invoke dance action
                self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['dance2']))
                
            elif self.keyverb == 'fly':                
                #invoke fly action
                self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['fly']))

            elif self.keyverb == 'pushup':
                #invoke pushup action
                self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['pushup']))

            elif self.keyverb == 'fight':
                #invoke fighting action
                #-self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_angry']))
                #-self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['karatekid']))
                #-self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['weirdgesture1']))
                self.(pose=self.asyn.readMotion(self.motionFilePath['pose_angry']), motionbuffer=self.asyn.readMotion(self.motionFilePath['karatekid']))
                self.updateFparam(pose=self.asyn.readMotion(self.motionFilePath['pose_angry']), motionbuffer=self.asyn.readMotion(self.motionFilePath['weirdgesture1']))

            if self.emotion == 'mad' or self.emotion == 'angry':
                print "mad / angry: set angry pose, sampling rate=3, gain++, interp tension++"
                
                #set angry pose
                #self.asyn.setMotionbuffer(self.asyn.readMotion(self.motionFilePath['pose_angry']))
                self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_angry']))
                
                #set (sampling) rate = 3
                self.asyn.setRate(3)
                
                #set gain ++ (higher)
                self.asyn.getFparam('gainslow')
                self.asyn.getFparam('gainsmed')
                self.asyn.getFparam('gainshigh')
                
                #set interp tension ++ (higher)
                self.asyn.getFparam('interptension')
                self.asyn.setInterpTension(2)
                
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

                self.updateFparam(rate=3, gainsmed=0, interpcontinuity=2, interptension=1.5)
                
            elif self.emotion == 'sad' or self.emotion == 'tired' or self.emotion == 'bored':
                print "sad / tired / bored: set tired pose, gain--"
                
                #set tired pose
                #-self.asyn.setAction('pose', self.asyn.readMotion(self.motionFilePath['pose_tired']))
                
                #set gain --
                self.asyn.getFparam('gainslow')
                self.asyn.getFparam('gainsmed')
                self.asyn.getFparam('gainshigh')

                self.updateFparam(pose=self.asyn.readMotion(self.motionFilePath['pose_tired']), gainslow=-2, gainsmed=-2, gainshigh=-2)

            elif self.emotion == 'calm':
                #self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['se_surfright']))
                #self.asyn.setAction('motionbuffer', self.asyn.readMotion(self.motionFilePath['se_surfleft']))
                
                #-self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['se_surfright']))
                #-self.updateFparam(motionbuffer=self.asyn.readMotion(self.motionFilePath['se_surfleft']))
                #-self.asyn.concatMotion()

                concatmotion = self.asyn.concatMotion2(self.asyn.readMotion(self.motionFilePath['se_surfright']),self.asyn.readMotion(self.motionFilePath['se_surfleft']))
                self.updateFparam(motionbuffer=concatmotion, gainshigh=-1, interpcontinuity=1)
                
            else:
                
                print "update", update
            
        else:
            
            print "update", update
        return update

    def updateFparam(self, motionbuffer=None, pose=None, interpbias=0, interptension=0, interpcontinuity=0, rate=1, gainslow=1, gainsmed=1, gainshigh=1, fftlow=1, ffthigh=1):
        if motionbuffer is None:
            motionbuffer = self.asyn.readMotion(self.motionFilePath['home'])
        self.asyn.('motionbuffer', motionbuffer)
        if pose is None:
            pose = self.asyn.readMotion(self.motionFilePath['pose_relax'])
        self.asyn.setAction('pose', pose)
        self.asyn.setInterpBias(interpbias)
        self.asyn.setInterpTension(interptension)
        self.asyn.setInterpContinuity(interpcontinuity)
        self.asyn.setRate(rate)
        return 1                

    def getMotionResponse(self):
        print "getMotionResponse()"    #Test
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

    def executeAllMotion(self):
        for each_motion in self.fpram['motionbuffer']:
            #apply gain adjustments to each_motion (original data) << be careful about this...
            #interpolate each_motion
            #apply resample, if any
            #apply other transformations, if any
            pass
        #concatenate all the transformed motion
        #save the concatenated motion

        return 1

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
