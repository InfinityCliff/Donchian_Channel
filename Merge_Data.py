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
#-----------------------------------------------------------------
# read data
#-----------------------------------------------------------------
if read_indicator:
    indicator = pickle_read(datapath, MagicNumber, 
        'indicator_wStats.pickle', 
        'Reading Indicator data')

if read_order:
    orders = pickle_read(datapath, MagicNumber, 
        'orders_wStats.pickle', 
        'Reading Order data')

if read_history:
    history = pickle_read(datapath, MagicNumber, 
        'history_wStats.pickle', 
        'Reading History data')

#-----------------------------------------------------------------
# merge history and indicator files, both have same number of rows
# both from on new bar
#-----------------------------------------------------------------
if read_history:
    history_M_Indicator = pd.merge(history, indicator, on='DateTime', how='left')
    history_M_Indicator.rename(columns={'Seconds_x': 'Seconds'}, inplace=True)
    history_M_Indicator.drop('Seconds_y', axis=1, inplace=True)

if read_order:
    order_M_indicator = pd.merge(orders, indicator, on='DateTime', how='left')


#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------
if read_history:
    pickle_write(history_M_Indicator, datapath, MagicNumber, 
        'history_M_indicator.pickle', 
        'Pickling History Data merged with Indicator')
    
if read_order:
    pickle_write(order_M_indicator, datapath, MagicNumber, 
        'order_M_indicator.pickle',
        'Pickling Order Data merged with Indicator')

#-----------------------------------------------------------------
# plot data
#-----------------------------------------------------------------
# history_M_Indicator.set_index('DateTime', inplace=True)
# history_M_Indicator['Low'].plot()
# history_M_Indicator['DOCS(25)'].plot()
# plt.show()
