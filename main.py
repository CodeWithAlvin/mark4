from utills.conditions import *
import sys



def start():
    user=functions.input_.voice_recognizer()
    output=Process(user)
    if any(i in user for i in ["exit","stop","cancel","quit"]) and output==None:
        sys.exit()
    functions.output.speech_out(output)
    
   
while True:
    try:
        start()
    except:
        continue











