import speechd, time

class CallbackExample(object):
    def __init__(self):
        self._client = speechd.SSIPClient('callback-test')

    def speak(self, text):
        def callback(callback_type):
            if callback_type == speechd.CallbackType.BEGIN:
                print "Speech started:", text
            elif callback_type == speechd.CallbackType.END:
                print "Speech completed:", text
            elif callback_type == speechd.CallbackType.CANCEL:
                print "Speech interrupted:", text
        self._client.speak(text, callback=callback, event_types=(speechd.CallbackType.BEGIN, speechd.CallbackType.CANCEL, speechd.CallbackType.END))

    def go(self):
        self.speak("Hi!")
        self.speak("How are you?")
        time.sleep(4) #wait for events to happen
        self._client.close()

CallbackExample().go()
