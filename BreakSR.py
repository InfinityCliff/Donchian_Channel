import sys
import numpy as np
import pandas as pd
from Functions import datapath

print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# Functions
#-----------------------------------------------------------------
def break_support(price, support):
    if price < support:
        return True
    else:
        return False

def break_resistance(price, resistance):
    if price > resistance:
        return True
    else:
        return False

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# read data
#-----------------------------------------------------------------
print('Reading Indicator data')
indicator = pd.read_pickle(datapath + 'indicator_wStats.pickle')

# print('Reading Order data')
# orders = pd.read_pickle(datapath + 'orders_wStats.pickle')

print('Reading Price History data')
history = pd.read_pickle(datapath + 'history_wStats.pickle')

#-----------------------------------------------------------------
# merge history and indicator files, both have same number of rows
# both from on new bar
#-----------------------------------------------------------------
history_M_Indicator = pd.merge(history, indicator, on='DateTime', how='left')
history_M_Indicator.rename(columns={'Seconds_x': 'Seconds'}, inplace=True)
history_M_Indicator.drop('Seconds_y', axis=1, inplace=True)

#-----------------------------------------------------------------
# determine when price breaks support and resistance lines
#-----------------------------------------------------------------
history_M_Indicator['Break_Support'] = list(map(break_support,
                                                history_M_Indicator['Low'],
                                                history_M_Indicator['DOCS(25)'].shift(1)))
history_M_Indicator['Break_Resistance'] = list(map(break_resistance,
                                                   history_M_Indicator['High'],
                                                   history_M_Indicator['DOCR(25)'].shift(1)))

#-----------------------------------------------------------------
# print summary data
#-----------------------------------------------------------------
print('Number of Bars that break Resistance Line:')
print(history_M_Indicator[(history_M_Indicator['Break_Resistance'] == True)]['Break_Resistance'].count())
print('Number of Bars that break Support Line:')
print(history_M_Indicator[(history_M_Indicator['Break_Support'] == True)]['Break_Support'].count())
print('Total Number of Bars')
print(len(history_M_Indicator))


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
