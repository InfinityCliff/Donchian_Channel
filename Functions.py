import datetime as dt

#-----------------------------------------------------------------
# Common Variables
#-----------------------------------------------------------------
datapath = "../Donchian_Channel_data/"

#-----------------------------------------------------------------
# function to convert 'DateTime' to seconds
#-----------------------------------------------------------------
def seconds(time):
    return (time - dt.datetime(1970, 1, 1)).total_seconds()