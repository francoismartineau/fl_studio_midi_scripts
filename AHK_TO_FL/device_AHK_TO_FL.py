# name=AHK_TO_FL
"""
    This midi script allows for communications between FLahk and FL Studio using midi messages.
    Some functions return midi responses to FLahk. To allow this:
    .Create a loopBack midi port named FL_TO_AHK
    .In FL Midi settings, disable it from the inputs
    .Meanwhile, the current loopBack midi port (AHK_TO_FL) should be enabled in the inputs and given a port number
    .In the outputs, give FL_TO_AHK the same port number as AHK_TO_FL. Give no port to AHK_TO_FL.
"""
import device, midi, mixer, patterns, transport, channels
import time

global transport_flush_time
transport_flush_time = time.time()

# -- Unidirectionnal funcs --------------------------------------------------------
def set_pattern(n):
    if type(n) is str and n.isdigit():
        n = int(n)
    if type(n) is int:
        patterns.jumpToPattern(n)
        print("set_pattern:", n)

def set_mixer_track_route(n):
    if type(n) is str and n.isdigit():
        n = int(n)
    currTrack = mixer.trackNumber()
    for dest in range(mixer.trackCount()):
        active = mixer.getRouteSendActive(currTrack, dest)
        if active:
            mixer.setRouteTo(currTrack, dest, 0)
    mixer.setRouteTo(currTrack, n, 1)
    mixer.getRouteSendActive(currTrack, n)
    print("set_mixer_track_route:", n)

def set_mixer_track(n):
    mixer.deselectAll()
    mixer.setTrackNumber(n)
    print("set_mixer_track:", n)

def toggle_play_pause_twice(_):
    toggle_play_pause(_)
    toggle_play_pause(_)

def stop(_):
    print("stop")
    transport.globalTransport(midi.FPT_Stop, 1)
    set_transport_flush_time()

def toggle_rec(_):
    print("toggle_rec")
    transport.globalTransport(midi.FPT_Record, 1)  

def toggle_play_pause(_):
    print("toggle_play_pause")
    transport.globalTransport(midi.FPT_Play, 1)
    set_transport_flush_time()

saved_song_pos = 0
def save_load_song_pos(save_load):
    global saved_song_pos
    if save_load == 1:
        print("save_song_pos")
        saved_song_pos = transport.getSongPos(midi.SONGLENGTH_ABSTICKS)
    elif save_load == 0:
        print("load_song_pos")
        transport.setSongPos(saved_song_pos, midi.SONGLENGTH_ABSTICKS)

def deselect_all_channels(_):
    channels.deselectAll()

# -- Bidirectionnal funcs --------------------------------------------------------
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

def get_bpm(_):
    bpm = mixer.getCurrentTempo(1)
    bpm = int(bpm)
    return bpm
# ----

functions = {
    127 : get_pattern,
    126 : set_pattern,
    125 : set_mixer_track_route,
    124 : get_mixer_track,
    123 : set_mixer_track,
    122 : toggle_play_pause_twice,
    121 : stop,
    120 : toggle_rec,
    119 : toggle_play_pause,
    118 : save_load_song_pos,
    117 : deselect_all_channels,
    116 : get_bpm,
    #115 : used to communicate with pd,
    
    50 : test_FL,
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
            if (answer is not None):
                send(answer)
        elif chan == 16 or (chan < 15 and time_since_transport_flush() < .1):
            event.handled = True
        else:
            print_event(event)

# ------------------------------------------------------
def set_transport_flush_time():
    global transport_flush_time
    transport_flush_time = time.time()

def time_since_transport_flush():
    global transport_flush_time
    return time.time() - transport_flush_time

def print_event(event):
    chan = event.midiChan + 1
    cc = event.controlNum
    val = event.controlVal
    handled = ""
    if event.handled:
        handled = "already handled"
    msg = "{}  chan: {}    cc: {}    val: {}".format(handled, chan, cc, val)
    print(msg)

def rand(min, max):
    seed = time.time()
    return min + int((seed *  761) % 997) % (max - min)

def send(answer):
    # 0xB : it's a cc message
    # 0x F: sent on chan 16
    # 127 : cc 127
    print("-> Chan 16, CC 127, VAL " + str(answer))
    sendMidiBytes(0xBF, 127, answer)

def sendMidiBytes(byte1, byte2, byte3):
    msg = byte1 + (byte2 << 8) + (byte3 << 16)
    device.midiOutMsg(msg)

print("-----------------------------------------------" + "|" * rand(1, 10))
