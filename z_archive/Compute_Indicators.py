import pandas as pd

from z_archive.Indicators import computeMACD as MACD
from z_archive.Indicators import roc, rsi

history = pd.read_pickle('data/history_wTrends.pickle')


history['MACD_slow'], history['MACD_fast'], history['MACD'] = MACD(history['Close'])
history['ROC'] = roc(history['Close'])
history['RSI'] = rsi(history['Close'])
print(history[['DateTime', 'Close', 'RSI']].tail(21))
