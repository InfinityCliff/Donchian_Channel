import sys
import numpy as np
import pandas as pd
import os.path
import time
from Functions import datapath, read_history, read_indicator, read_order, MagicNumber

print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)


#-----------------------------------------------------------------
#-----------------------------------------------------------------
# read data
#-----------------------------------------------------------------
if read_indicator:
    print('Reading Indicator data')
    file = datapath + MagicNumber + '_indicator_wStats.pickle'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    indicator = pd.read_pickle(file)

if read_order:
    print('Reading Order data')
    file = datapath + MagicNumber + '_orders_wStats.pickle'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    orders = pd.read_pickle(file)

if read_history:
    print('Reading Price History data')
    file = datapath + MagicNumber + '_history_wStats.pickle'
    print('-> reading -- ' + file)
    print("       mod -- %s" % time.ctime(os.path.getmtime(file)))
    history = pd.read_pickle(file)

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
    print(order_M_indicator.head())


#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------

print('Pickling History Data merged with Indicator')
history_M_Indicator.to_pickle(datapath + 'history_M_Indicator.pickle')


#-----------------------------------------------------------------
# plot data
#-----------------------------------------------------------------
# history_M_Indicator.set_index('DateTime', inplace=True)
# history_M_Indicator['Low'].plot()
# history_M_Indicator['DOCS(25)'].plot()
# plt.show()
