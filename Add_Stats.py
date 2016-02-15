import sys
import numpy as np
import pandas as pd
import os.path
import time
from Functions import datapath
from Init_pickle_Data import MagicNumber, read_history, read_indicator, read_order

print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

#-----------------------------------------------------------------
# Add Rolling stats to dataframe
#-----------------------------------------------------------------
def add_rolling_stats(dataframe, fields, window=15, head=False):
    # TODO - add keyword args to determine which stats to apply
    for field in fields:
        #dataframe['Roll_Profit_Count'] = pd.rolling_apply(dataframe[field], window, rolling_profit_count, 1)
        dataframe[field + '-Roll_Mean'] = pd.rolling_mean(dataframe[field], window)
        dataframe[field + '-Roll_std'] = pd.rolling_std(dataframe[field], window)
        dataframe[field + '-Roll_var'] = pd.rolling_var(dataframe[field], window)
    # Order Dataframe with Trends added
    if head:  # print head if passed value
        dataframe[['DateTime', 'Ticket', 'Profit', 'Trend', 'Roll_Profit_Count', 'Roll_Mean', 'Roll_std']].head(head)
    return dataframe

#-----------------------------------------------------------------
# function returns sum of count of number of profit (+1) and loss trades (-1)
#-----------------------------------------------------------------
def rolling_profit_count(dataframe):
    count = 0
    for profit in dataframe:
        if profit >= 0:
            # count = count + 1
            count += 1
        else:
            count += 1  # = count -1
    return count


#-----------------------------------------------------------------
#-----------------------------------------------------------------
# read data
#-----------------------------------------------------------------
if read_indicator:
    print('Reading Indicator data')
    file = datapath + MagicNumber + '_indicator.pickle'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    indicator = pd.read_pickle(file)
    cols = indicator.columns.tolist()  # get rid of ambiguous columns 'Ticket', 'Open/Close'
    cols = cols[0:2] + cols[4:]
    indicator = indicator[cols]

if read_order:
    print('Reading Order data')
    file = datapath + MagicNumber + '_orders.pickle'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    orders = pd.read_pickle(file)

if read_history:
    print('Reading Price History data')
    file = datapath + MagicNumber + '_history.pickle'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    history = pd.read_pickle(file)
#print(history.tail())

#-----------------------------------------------------------------
# add Stats
#-----------------------------------------------------------------
add_rolling_stats(indicator, indicator.columns[4:])
add_rolling_stats(history, ['Close'])

#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------
if read_indicator:
    print('Pickling Indicator Data with Stats')
    file = datapath + MagicNumber + '_indicator_wStats.pickle'
    print('-> writing -- ' + file)
    indicator.to_pickle(file)

if read_order:
    print('Pickling Order Data with Stats')
    file = datapath + MagicNumber + '_orders_wStats.pickle'
    print('-> writing -- ' + file)
    orders.to_pickle(file)

if read_history:
    print('Pickling History Data with Stats')
    file = datapath + MagicNumber + '_history_wStats.pickle'
    print('-> writing -- ' + file)
    history.to_pickle(file)
