from Communications import Protocols
import time

PIobj = Protocols.PIobj
BeatDuration = 0.11
PWM_DutyCycle = 127

class BuzzerObj(object):

    def __init__(self,buzzerPin):
        self.pin = buzzerPin
        self.isPlaying = False

    def PlayMelody(self, melody):
        self.isPlaying = True
        for n in melody.notes:
            self.PlayNote(n)
        self.isPlaying = False
        return

    def PlayNote(self, note):
        PIobj.set_PWM_dutycycle(self.pin,PWM_DutyCycle)
        PIobj.set_PWM_frequency(self.pin,note.pitch)
        time.sleep(note.beat*BeatDuration)
        PIobj.set_PWM_dutycycle(self.pin,0)
        time.sleep(note.air*BeatDuration)
        return

class Note(object):

    def __init__(self,pitch=10,beat=1,air=0):
        self.pitch = pitch #min freq
        self.beat = beat
        self.air = air

class Melody:
    notes = None #list cannot be init


AngryMelody = Melody()
HappyMelody = Melody()
NormalMelody = Melody()
SadMelody = Melody()

#AngryMelody.notes = [Note(8000,6,1),Note(6000,1,1),Note(6000,1,2),Note(200,4,1),Note(50,8,4),Note(200,4,1),Note(50,8)]
AngryMelody.notes = [Note(200,4,1),Note(50,8,4),Note(200,4,1),Note(50,8,4),Note(200,4,1),Note(50,8)]
HappyMelody.notes = [Note(700,1,1),Note(1000,1),Note(1500,1,2),Note(700,1,1),Note(1000,1),Note(1500,1,2),
Note(5000,1),Note(6000,2),Note(8000,1,2),Note(5000,1),Note(6000,2),Note(8000,1)] #TODO make it whistling
NormalMelody.notes = [Note(100,2),Note(50,1)]
SadMelody.notes = [Note(200,1,1), Note(75,6,2), Note(150,1,1), Note(50,1,1), Note(50,4)]
