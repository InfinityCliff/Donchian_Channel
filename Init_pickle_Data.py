import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from Functions import seconds, datapath

print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

MagicNumber = "150000"

#-----------------------------------------------------------------
# read in Indicator data into dataframe
#-----------------------------------------------------------------
def read_indicator_data(head=False):
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
    dataframe = pd.read_csv(datapath + 'EURUSD1_2015.csv', header=None)
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

print('Reading Indicator data')
indicator = read_indicator_data()

#print('Reading Order data')
# orders = read_order_data()
#plot_order_data()

print('Reading Price History data')
start = dt.datetime(2015, 1, 1)
end = dt.datetime(2015, 12, 31)
history = read_price_history(start, end)

#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------
print('Pickling Indicator Data')
indicator.to_pickle(datapath + 'indicator.pickle')

#print('Pickling Order Data')
# orders.to_pickle('data/orders.pickle')

print('Pickling History Data')
history.to_pickle(datapath + 'history.pickle')
