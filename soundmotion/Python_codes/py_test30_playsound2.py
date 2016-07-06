import pymedia
import time

demuxer = pymedia.muxer.Demuxer('mp3')

f = open('/home/msunardi/Desktop/Downloads/bugs_mail.mp3', 'rb')


spot = f.read()
frames = demuxer.parse(spot)
print 'read it has %i frames' % len(frames)
decoder = pymedia.audio.acodec.Decoder(demuxer.streams[0])
frame = decoder.decode(spot)
print dir(frame)
sound = pymedia.audio.sound
print frame.bitrate, frame.sample_rate
song = sound.Output( frame.sample_rate, frame.channels, 16 )

while len(spot) > 0:
    try:
        if frame: 
            song.play(frame.data)
            print "Position: ", song.getPosition(), "GetLeft: ", song.getLeft()
        spot = f.read(512)
        frame = decoder.decode(spot)
    except:
        pass
   
while song.isPlaying(): time.sleep(.05)
print 'well done' 
