import aiml
import speechd

k = aiml.Kernel()
k.learn("/home/msunardi/standard/std-hello.aiml")
k.learn("/home/msunardi/standard/std-65percent.aiml")
k.learn("/home/msunardi/standard/std-atomic.aiml")
k.learn("/home/msunardi/standard/std-botmaster.aiml")
k.learn("/home/msunardi/standard/std-brain.aiml")
k.learn("/home/msunardi/standard/std-connect.aiml")
k.learn("/home/msunardi/standard/std-dictionary.aiml")
k.learn("/home/msunardi/standard/std-disconnect.aiml")
k.learn("/home/msunardi/standard/std-dont.aiml")
k.learn("/home/msunardi/standard/std-errors.aiml")
k.learn("/home/msunardi/standard/std-gender.aiml")
k.learn("/home/msunardi/standard/std-geography.aiml")
k.learn("/home/msunardi/standard/std-german.aiml")
k.learn("/home/msunardi/standard/std-gossip.aiml")
k.learn("/home/msunardi/standard/std-inactivity.aiml")
k.learn("/home/msunardi/standard/std-inventions.aiml")
k.learn("/home/msunardi/standard/std-knowledge.aiml")
k.learn("/home/msunardi/standard/std-lizards.aiml")
k.learn("/home/msunardi/standard/std-login.aiml")
k.learn("/home/msunardi/standard/std-numbers.aiml")
k.learn("/home/msunardi/standard/std-personality.aiml")
k.learn("/home/msunardi/standard/std-pickup.aiml")
k.learn("/home/msunardi/standard/std-politics.aiml")
k.learn("/home/msunardi/standard/std-profile.aiml")
k.learn("/home/msunardi/standard/std-religion.aiml")
k.learn("/home/msunardi/standard/std-robot.aiml")
k.learn("/home/msunardi/standard/std-sales.aiml")
k.learn("/home/msunardi/standard/std-sextalk.aiml")
k.learn("/home/msunardi/standard/std-sports.aiml")
k.learn("/home/msunardi/standard/std-srai.aiml")
k.learn("/home/msunardi/standard/std-suffixes.aiml")
k.learn("/home/msunardi/standard/std-that.aiml")
k.learn("/home/msunardi/standard/std-turing.aiml")
k.learn("/home/msunardi/standard/std-yesno.aiml")
#k.respond("load aiml b")

client = speechd.SSIPClient('test')


while True:
    response = k.respond(raw_input("> "))
    #print k.respond(raw_input("> "))
    print response
    
    client.speak(response)
    
client.stop()
client.close()    
