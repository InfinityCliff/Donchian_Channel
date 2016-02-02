import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import functools
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
price_data['DOCS25_sft1'] = price_data['DOCS(25)'].shift(1)

#-----------------------------------------------------------------
# Functions
#-----------------------------------------------------------------

def br_check_profit_loss_SELL(df, BR):
    c = 0
    if not BR:
        SELL = 'NO ORDER'
    else:
        SELL = ''
    while SELL == '':
        ind = np.where(df.Break_Resistance == True)

        if SELL == '':
            #print('s1--------------------------------------------')
            for i in np.nditer(ind):
                subdf = df.loc[int(i):]
                #print(subdf[['DateTime', 'High', 'Low', 'DOCS(25)', 'DOCR(25)', 'DOCS25_sft1',
                #'Break_Support', 'Break_Resistance']])
                sl_sell = subdf.High.iloc[0] + (sl * point * xecn)
                #print('ORDER PRICE', subdf.High.iloc[0], 'sl_sell', sl_sell)
                # Break resistance, SELL check for profit
                p = np.where(subdf.Low <= subdf.DOCS25_sft1)[0]
                # Break resistance, SELL check for loss
                l = np.where(subdf.High > sl_sell)[0]
                #print('p', p, 'l', l)
                if (p.size > 0) & (l.size > 0):
                    if p.min() < l.min():
                        SELL = 'PROFIT'
                    if l.min() < p.min():
                        SELL = 'LOSS'
                elif (p.size > 0) & (l.size == 0):
                    SELL = 'PROFIT'
                elif (p.size == 0) & (l.size > 0):
                    SELL = 'LOSS'
                elif (p.size ==0 ) & (l.size == 0):
                    SELL = 'UNK'
                    #input('Enter to continue SELL')
    c += 1
    #print('c=', c)
    return SELL

def br_check_profit_loss_BUY(df, BR):
    c = 0
    #print('br:', BR)
    if not BR:
        BUY = 'NO ORDER'
    else:
        BUY = ''
    while (BUY == ''):
        c += 1
        ind = np.where(df.Break_Resistance == True)
        if BUY == '':
            #print('b1--------------------------------------------')
            for i in np.nditer(ind):
                subdf = df.loc[int(i):]
                #print(subdf[['DateTime', 'High', 'Low', 'DOCS(25)', 'DOCR(25)', 'DOCS25_sft1',
                #'Break_Support', 'Break_Resistance']])
                tp_buy = subdf.High.iloc[0] + (tp * point * xecn)
                sl_buy = subdf.High.iloc[0] - (sl * point * xecn)
                #print('ORDER PRICE', subdf.High.iloc[0], 'tp_buy', tp_buy, 'sl_buy', sl_buy)
                # Break resistance, BUY check for profit
                p = np.where(subdf.High >= tp_buy)[0]
                # Break resistance, BUY check for loss
                l = np.where(subdf.Low <= sl_buy)[0]
                #print('p', p, 'l', l)
                if (p.size > 0) & (l.size > 0):
                    if p.min() < l.min():
                        BUY = 'PROFIT'
                    if l.min() < p.min():
                        BUY = 'LOSS'
                elif (p.size > 0) & (l.size == 0):
                    BUY = 'PROFIT'
                elif (p.size == 0) & (l.size > 0):
                    BUY = 'LOSS'
                elif (p.size ==0 ) & (l.size == 0):
                    BUY = 'UNK'
    return BUY

#-----------------------------------------------------------------
# check if would be Profit or Loss
#-----------------------------------------------------------------
price_data['BR_BUY'] = list(map(functools.partial(br_check_profit_loss_BUY, price_data), price_data.Break_Resistance))
price_data['BR_SELL'] = list(map(functools.partial(br_check_profit_loss_SELL, price_data), price_data.Break_Resistance))
