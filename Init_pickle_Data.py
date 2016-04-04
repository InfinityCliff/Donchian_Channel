import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import time
import datetime as dt
from Functions import seconds, datapath, read_history, read_indicator, read_order, MagicNumber, pickle_write

print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

#-----------------------------------------------------------------
# Init variables
#-----------------------------------------------------------------
history_file_name = 'EURUSD30.csv'

#-----------------------------------------------------------------
# read in Indicator data into dataframe
#-----------------------------------------------------------------
def read_indicator_data(head=False):
    file = datapath + MagicNumber + '_Indicators.csv'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    dataframe = pd.read_csv(datapath + MagicNumber + '_Indicators.csv')
    dataframe.rename(columns={'Date': 'DateTime'}, inplace=True)      # rename 'Date' column to 'DateTime'
    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])     # convert 'DateTime' to pd.datetime
    dataframe['Seconds'] = list(map(seconds, dataframe['DateTime']))  # calc seconds

    #split apart datetime into date and time columns
    #temp = pd.DatetimeIndex(dataframe['DateTime'])
    #dataframe['Date'] = temp.date
    #dataframe['Time'] = temp.time

    cols = dataframe.columns.tolist()           # rearrange to put 'Date' and 'Time' up front behind 'DateTime'
    cols = cols[0:1] + cols[-1:] + cols[1:-1]   #
    dataframe = dataframe[cols]                 #

    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])
    if head:
        print(dataframe.head(head))    
    return dataframe

#-----------------------------------------------------------------
# read in order data into dataframe
#-----------------------------------------------------------------
def read_order_data(head=False):
    file = datapath + MagicNumber + '_Orders.csv'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    dataframe = pd.read_csv(datapath + MagicNumber + '_Orders.csv')
    dataframe['DateTime'] = dataframe['Open Time']  # Copy 'Open Time' to 'DateTime' and preserve original
    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])     # convert 'DateTime' to pd.datetime
    dataframe['Seconds'] = list(map(seconds, dataframe['DateTime']))  # calc seconds
    dataframe = dataframe[['DateTime', 'Seconds', 'Ticket', 'Profit', 'Type', 'Lots', 'Symbol', 'Open Price',
                           'StopLoss', 'TakeProfit', 'Close Price', 'Commission', 'Swap', 'Open Time',
                           'Close Time']]  # rearrange column orders
    if head:  # print head if passed value
        print(dataframe.head(head))
    return dataframe
    
#-----------------------------------------------------------------
# read in price history into dataframe
#-----------------------------------------------------------------
def read_price_history(start_date, end_date, head=False):
    file = datapath + history_file_name
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    dataframe = pd.read_csv(file, header=None)
    dataframe.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ticks']  # Name Columns
    dataframe['DateTime'] = dataframe['Date'] + ' ' + dataframe['Time']  # Combine 'Date' and 'Time' to 'DateTime'
    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])        # convert 'DateTime' to pd.datetime
    dataframe = dataframe[((dataframe['DateTime'] > start_date) &
                           (dataframe['DateTime'] < end_date))]           # filter to start and end dates
    dataframe['Seconds'] = list(map(seconds, dataframe['DateTime']))     # calc seconds
    dataframe = dataframe[['DateTime', 'Seconds', 'Date', 'Time', 'Open',
                           'High', 'Low', 'Close', 'Ticks']]  # rearrange column order
    if head:  # print head if passed value
        print(dataframe.head(head))
    return dataframe
 
#-----------------------------------------------------------------
# Plot Order Data - creation of graph to visually determine trend ranges
#-----------------------------------------------------------------
def plot_order_data(orders_data):
    #plot rolling data, intent was to determine range of UP, DOWN and FLAT for next step
    plt.plot(orders_data['Ticket'], orders_data['Roll_std'])
    plt.plot(orders_data['Ticket'], orders_data['Profit'], marker='x', linestyle=':')
    
    plt.show()

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
print('-----------------------------------------------------------------')
if read_indicator:
    print('Reading Indicator data')
    indicator = read_indicator_data()

if read_order:
    print('Reading Order data')
    orders = read_order_data()
    # plot_order_data()

if read_history:
    print('Reading Price History data')
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime(2015, 12, 31)
    history = read_price_history(start, end)

#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------
print('-----------------------------------------------------------------')
if read_indicator:
    pickle_write(indicator, datapath, MagicNumber, 
        'indicator.pickle', 
        'Pickling Indicator Data')

if read_order:
    pickle_write(orders, datapath, MagicNumber, 
        'orders.pickle', 
        'Pickling Indicator Data')    

if read_history:
    pickle_write(history, datapath, MagicNumber, 
        'history.pickle', 
        'Pickling Price History Data')    

