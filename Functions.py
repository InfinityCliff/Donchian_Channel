import sys
import pandas as pd
import datetime as dt
import winsound
import os.path
import time

#-----------------------------------------------------------------
# Common Variables
#-----------------------------------------------------------------
MagicNumber = "160002"
datapath = "data/" + MagicNumber + "/"
read_indicator = True
read_history = True
read_order = False

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