import sys
import numpy as np
import pandas as pd
from Functions import datapath

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

print('Reading Indicator data')
indicator = pd.read_pickle(datapath + 'indicator.pickle')
#print(indicator.tail())
# get rid of ambiguous columns 'Ticket', 'Open/Close'
cols = indicator.columns.tolist()
cols = cols[0:2] + cols[4:]
indicator = indicator[cols]
#print(indicator.head())

# print('Reading Order data')
# orders = pd.read_pickle('data/orders.pickle')

print('Reading Price History data')
history = pd.read_pickle(datapath + 'history.pickle')
#print(history.tail())

#-----------------------------------------------------------------
# add Stats
#-----------------------------------------------------------------
add_rolling_stats(indicator, indicator.columns[4:])
add_rolling_stats(history, ['Close'])

#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------
print('Pickling Indicator Data with Stats')
indicator.to_pickle(datapath + 'indicator_wStats.pickle')

#print('Pickling Order Data with Stats')
# orders.to_pickle(datapath + 'orders_wStats.pickle')

print('Pickling History Data with Stats')
history.to_pickle(datapath + 'history_wStats.pickle')
