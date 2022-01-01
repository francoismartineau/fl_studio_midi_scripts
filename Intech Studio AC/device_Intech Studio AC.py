# name=Oxygen 25
import device, midi, mixer, patterns, transport, channels
import time

def OnMidiMsg(event):
    global functions
    if (not event.handled): 
        
        chan = event.midiChan + 1
        if chan == 15:
            event.handled = True
            ctl_num = event.controlNum
            print(ctl_num)
            print("----------------------------")
        print_event(event)