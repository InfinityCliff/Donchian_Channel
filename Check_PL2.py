import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

style.use('fivethirtyeight')

point = 0.0001
xecn = 10
sl = 50
tp = 50

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# read data
#-----------------------------------------------------------------

print('Reading Price data')
price_data = pd.read_pickle('data/history_M_Indicator.pickle')

#-----------------------------------------------------------------
# Functions
#-----------------------------------------------------------------

def check_profit_loss(df):
    print(df.head())
    sl_sell = df['High'] + sl * point * xecn
    sl_buy = df['High'] - sl * point * xecn
    tp_buy = df['High'] + tp * point * xecn
    c = -1
    SELL = BUY = ''
    while (SELL == '') & (BUY == ''):
        # Break resistance, SELL check for profit
        if df['Low'].shift(c) <= df['DOCS(25)'].shift(c):
            SELL = 'PROFIT'
        # Break resistance, SELL check for loss
        if df['High'].shift(c) >= sl_sell:
            SELL = 'LOSS'
        # Break resistance, BUY check for profit
        if df['High'].shift(c) >= tp_buy:
            BUY = 'PROFIT'
        # Break resistance, BUY check for loss
        if df['Low'].shift(c) <= sl_buy:
            BUY = 'LOSS'
        c -= 1
    return BUY, SELL

#-----------------------------------------------------------------
# check if would be Profit or Loss
#-----------------------------------------------------------------
BS = price_data[(price_data['Break_Support'] == True)][['DateTime',
                                                        'Open', 'High', 'Low', 'Close',
                                                        'DOCS(25)', 'DOCR(25)']]
print(BS.head())
print('Running Check on Breaking Support')
price_data[['BUY_PL', "SELL_PL"]] = list(map(check_profit_loss, BS))
