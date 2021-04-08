# name=2
"""
    This midi script allows for communications between FLahk and FL Studio using midi messages.
    device_1 does unidirectional communication (FLahk to FL Studio)
    device_2 does bidirectional communication. FLahk asks questions to FL Studio, which answers back
"""
import device, midi, mixer, patterns, transport, channels
import time

global transport_flush_time
transport_flush_time = time.time()

# ----------------------------------------------------------
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

functions = {
    126 : set_pattern,
    125 : set_mixer_track_route,
    123 : set_mixer_track,
    122 : toggle_play_pause_twice,
    121 : stop,
    120 : toggle_rec,
    119 : toggle_play_pause,
    118 : save_load_song_pos,
    117 : deselect_all_channels
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
            functions[func](param)
        elif chan == 16 or (chan < 15 and time_since_transport_flush() < .1):
            event.handled = True
        print_event(event)

# ------------------------------------------------------
def set_transport_flush_time():
    global transport_flush_time
    transport_flush_time = time.time()

def time_since_transport_flush():
    global transport_flush_time
    return time.time() - transport_flush_time

def print_event(event):
    event.handled
    chan = event.midiChan + 1
    cc = event.controlNum
    val = event.controlVal
    handled = ""
    if event.handled:
        #handled = "x"
        msg = "x"
    else:
        msg = "{}  chan: {}    cc: {}    val: {}".format(handled, chan, cc, val)
    print(msg)

def rand(min, max):
    seed = time.time()
    return min + int((seed *  761) % 997) % (max - min)

print("-----------------------------------------------" + "|" * rand(1, 10))
