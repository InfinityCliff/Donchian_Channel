import sys
import pandas as pd
import datetime as dt
import winsound
import os.path
import time

#-----------------------------------------------------------------
# Common Variables
#-----------------------------------------------------------------
datapath = "data/"
MagicNumber = "160001"
read_indicator = True
read_history = False
read_order = True

#-----------------------------------------------------------------
# function to convert 'DateTime' to seconds
#-----------------------------------------------------------------
def seconds(time):
    return (time - dt.datetime(1970, 1, 1)).total_seconds()

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
    
def pickle_write(df, dpath, MN, name, message):
    print(message)
    file = dpath + MN + '_'+ name
    print('-> writing -- ' + file)
    df.to_pickle(file)
    
def pickle_read(dpath, MN, name, message):
    print(message)
    file = dpath + MN + '_' + name
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    df = pd.read_pickle(file)
    return df