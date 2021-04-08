# name=1
"""
    This midi script allows for communications between FLahk and FL Studio using midi messages.
    device_1 does unidirectionnal communication (FLahk to FL Studio)
    device_2 does the same and lets FL Studio answer
"""
import device, midi, mixer, patterns, transport, channels
import time

global transport_flush_time

# ----------------------------------------------------------
def test_FL(_):
    print("test_FL")
    return 49

def get_pattern(_):
    p = patterns.patternNumber()
    print("get_pattern:", p)
    return p

def get_mixer_track(_):
    n = mixer.trackNumber()
    print("get_mixer_track:", n)
    return n  

functions = {
    50 : test_FL,
    127 : get_pattern,
    124 : get_mixer_track,
}

# ----------------------------------------------------------
def OnMidiMsg(event):
    global functions
    if (not event.handled): 
        
        chan = event.midiChan + 1
        if chan == 15:
            event.handled = True
            func = event.controlNum
            param = event.controlVal
            print("----------------------------")
            answer = functions[func](param)
            send(answer)
        #print_event(event)



# ---------------------------------------------
def is_numpad(event):
    return event.controlNum == 100

def send(answer):
    # 0xB0: it's a cc messave
    # 0x0F: sent on chan 16
    # 127 : cc 127
    sendMidiBytes(0xBF, 127, answer)

def sendMidiBytes(byte1, byte2, byte3):
    msg = byte1 + (byte2 << 8) + (byte3 << 16)
    device.midiOutMsg(msg)

def print_event(event):
    event.handled
    chan = event.midiChan + 1
    cc = event.controlNum
    val = event.controlVal
    handled = ""
    if event.handled:
        handled = "x"
    msg = "{}  chan: {}    cc: {}    val: {}".format(handled, chan, cc, val)
    print(msg)

def rand(min, max):
    seed = time.time()
    return min + int((seed *  761) % 997) % (max - min)

print("-----------------------------------------------" + "|" * rand(1, 10))
