import sys
import numpy as np
import pandas as pd
import os.path
import time
from Functions import datapath, read_history, read_indicator, read_order, MagicNumber, pickle_write, pickle_read

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
    indicator = pickle_read(datapath, MagicNumber, 
        'indicator.pickle', 
        'Reading Indicator data')    
    cols = indicator.columns.tolist()  # get rid of ambiguous columns 'Ticket', 'Open/Close'
    cols = cols[0:2] + cols[4:]
    indicator = indicator[cols]

if read_order:
    orders = pickle_read(datapath, MagicNumber, 
        'orders.pickle', 
        'Reading Order data')

if read_history:
    history = pickle_read(datapath, MagicNumber, 
        'history.pickle', 
        'Reading History data')    

#-----------------------------------------------------------------
# add Stats
#-----------------------------------------------------------------
if read_indicator:
    print('Calculating stats for Indicator Data')
    add_rolling_stats(indicator, indicator.columns[4:])

if read_order:
    print('Calculating stats for Order Data')
    add_rolling_stats(orders, ('Open Price', 'Close Price', 'Profit'))

if read_history:
    print('Calculating stats for History Data')
    add_rolling_stats(history, ('Open', 'Close'))

#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------
if read_indicator:
    pickle_write(indicator, datapath, MagicNumber, 
        'indicator_wStats.pickle', 
        'Pickling Indicator Data with Stats added')

if read_order:
    pickle_write(orders, datapath, MagicNumber, 
        'orders_wStats.pickle', 
        'Pickling Order Data with Stats added')

if read_history:
    pickle_write(history, datapath, MagicNumber, 
        'history_wStats.pickle', 
        'Pickling Price History Data with Stats added')    

