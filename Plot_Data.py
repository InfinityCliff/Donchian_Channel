import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

history = pd.read_pickle('data/history.pickle')
orders = pd.read_pickle('data/orders.pickle')
indicator = pd.read_pickle('data/indicator.pickle')

print(indicator[(indicator['Ticket'] > 0)].head())
#orders['Profit'].plot(x='DateTime', kind='bar')
#plt.show()
