import pandas as pd

history = pd.read_pickle('data/history.pickle')
orders = pd.read_pickle('data/orders.pickle')
indicator = pd.read_pickle('data/indicator.pickle')

#print(orders.head())
# pulls indicator data for order open times
order_open = indicator[((indicator['Open/Close'] != 'Close') & (indicator['Ticket'] > 0))]
print(order_open.head())
