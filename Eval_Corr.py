import sys
import numpy as np
import pandas as pd
import os.path
import time
from Functions import datapath, read_history, read_order, MagicNumber, pickle_write, pickle_read

print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# read data
#-----------------------------------------------------------------
if read_order:
    orders = pickle_read(datapath, MagicNumber, 
        'order_M_indicator.pickle', 
        'Reading Order data')

if read_history:
    history = pickle_read(datapath, MagicNumber, 
        'history_M_Indicator.pickle', 
        'Reading History data')
        
#-----------------------------------------------------------------
#-----------------------------------------------------------------
# correlate data
#-----------------------------------------------------------------
if read_order:
    print('Correlating Order Data')
    order_cor = orders.corr()

if read_history:
    print('Correlating History Data')
    history_cor = history.corr()

