import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

df_Ind = pd.read_csv('data/150001_Indicators.csv', parse_dates=['Date'])
df_Orders = pd.read_csv('data/150001_Orders.csv', parse_dates=['Open Time'])

print(df_Ind.head())

