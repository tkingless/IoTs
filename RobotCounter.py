#Robot logic
# Expose two BLE characteristics. With notify and write, read attributes: Min(0-99), Sec(0-59)
# When state "C" received, start count
# Control LR eyes, mbits to display, buzzers
# counting var, counting down logic

#Controller logic
#There is default val of the two BLE chars
#Only when 'C' sent, Robot to count


import threading
import time

class RobotCounter(object):

    def __init__(self,robotd):
        self.counter = None
        self.onCntDelegates = []
        self.onCntFinishDelegates = []
        return

    def StartCountDown(self,mins,secs):

        #min max of mins and secs:
        mins = max(0,min(mins,99))
        secs = max(0,min(secs,59))

        self.counter = CounterObj(mins,secs)
        self.counter.InvokeCount = self.OnCountCB
        self.counter.InvokeCountFinish = self.OnCountFinishCB
        self.counter.start()
        return

    def StopCounting(self):
        self.counter.isAlive = False
        return

    def OnCountCB(self,argMin,argSec):
        print("bits should be: {0}".format(self.LRmbitsDigits(argMin,argSec))
        return

    def OnCountFinishCB(self):
        #ask the robotd to return Normal state
        return

    def LRmbitsDigits(self,argMin,argSec):
        Ldigit = None
        Rdigit = None
        if argMin is not 0:
            digits = format(argMin,'02d') #with 0 complement
            Rdigit = digits[0]
            Ldigit = digits[1]
        else:
            digits = format(argSec,'02d') #with 0 complement
            Rdigit = digits[0]
            Ldigit = digits[1]

        return (int(Rdigit),int(Ldigit))

class CounterObj(threading.Thread):

    def __init__(self,minCnt=1,secCnt=30):
        threading.Thread.__init__(self)
        self.minCnt = minCnt
        self.secCnt = secCnt
        self.isAlive = True

        self.InvokeCount = None
        self.InvokeCountFinish = None

    def run(self):
        minCur = self.minCnt
        secCur = self.secCnt

        while (minCur != 0 or secCur != 0) and self.isAlive is True:
            time.sleep(1)
            if secCur is not 0:
                secCur -= 1
            else:
                if minCur is not 0:
                    minCur -= 1
                    secCur = 59

            #print("minCur: {0}, secCur: {1}".format(minCur,secCur))
            self.InvokeCount(minCur,secCur)

        if self.isAlive is True:
            print("Count finished")
            self.InvokeCountFinish()
        else:
            print("Count Interrupted")

        return

    def InvokeCount(self,minCur,secCur):
        if self.InvokeCount is not None:
            self.InvokeCount(minCur,secCur)
        return

    def InvokeCountFinish(self):
        if self.InovkeCountFinish is not None:
            self.InvokeCountFinish()
        return

def Hello(a,b):
    print("hello world: {0}, {1}".format(a,b))
