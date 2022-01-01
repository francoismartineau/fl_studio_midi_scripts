# name=TouchDesigner
import midi, transport

def stop():
    print("stop")
    transport.globalTransport(midi.FPT_Stop, 1)

def toggle_rec():
    print("toggle_rec")
    transport.globalTransport(midi.FPT_Record, 1)  

def toggle_play_pause():
    print("toggle_play_pause")
    transport.globalTransport(midi.FPT_Play, 1)

functions = {
    121 : stop,
    120 : toggle_rec,
    119 : toggle_play_pause,
}
# ----------------------------------------

def OnMidiMsg(event):
    global functions
    if (not event.handled): 
        chan = event.midiChan + 1
        if chan == 15:
            event.handled = True
            ctl = event.controlNum + 1
            if (ctl in functions):
                functions[ctl]()
                print_event(event)
            else:
                print("ctl: " + str(ctl) + " has no function.")
            print("----------------------------")

def print_event(event):
    chan = event.midiChan + 1
    cc = event.controlNum
    val = event.controlVal
    handled = ""
    if event.handled:
        handled = "already handled"
    msg = "{}  chan: {}    cc: {}    val: {}".format(handled, chan, cc, val)
    print(msg)