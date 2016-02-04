import sys
import datetime as dt
import winsound

#-----------------------------------------------------------------
# Common Variables
#-----------------------------------------------------------------
datapath = "data/"

#-----------------------------------------------------------------
# function to convert 'DateTime' to seconds
#-----------------------------------------------------------------
def seconds(time):
    return (time - dt.datetime(1970, 1, 1)).total_seconds()

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)