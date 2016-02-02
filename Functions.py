import datetime as dt

#-----------------------------------------------------------------
# function to convert 'DateTime' to seconds
#-----------------------------------------------------------------
def seconds(time):
    return (time - dt.datetime(1970, 1, 1)).total_seconds()