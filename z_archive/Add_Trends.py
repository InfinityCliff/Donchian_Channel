import pandas as pd
from Functions import seconds

history = pd.read_pickle('data/history.pickle')
orders = pd.read_pickle('data/orders.pickle')
indicator = pd.read_pickle('data/indicator.pickle')

# Create Trend Ranges, based on visual inspection of previous graph, and add Trends to Order dataframe
trend_labels = ['UP1', 'FLAT1', 'DOWN1', 'UP2', 'DOWN2', 'FLAT2', 'DOWN3', 'UP3', 'DOWN4', 'UP4',
                'DOWN5', 'UP6', 'FLAT3']

trend_range_per_order_tickets = [0, 6, 33, 60, 77, 86, 150, 171, 207, 222, 271, 314, 331, 348]

trend_range_per_DateTime = list(orders[orders['Ticket'].isin(trend_range_per_order_tickets)]['DateTime'])
trend_range_per_Seconds = list(map(int, list(map(seconds, trend_range_per_DateTime))))

print('trend labels: ' + str(len(trend_labels)))
print('trend_range_per_order_tickets labels: ' + str(len(trend_range_per_order_tickets)))
print('trend trend_range_per_DateTime: ' + str(len(trend_range_per_DateTime)))
print('trend trend_range_per_Seconds: ' + str(len(trend_range_per_Seconds)))
print('------------------------')
firstOrder = orders['DateTime'][0]  # Add the 'first ticket time' to the Series
trend_range_per_DateTime.insert(0, firstOrder)
firstOrder = int(orders['Seconds'][0])
trend_range_per_Seconds.insert(0, firstOrder)

print('trend_range_per_order_tickets')
print(trend_range_per_order_tickets)
print()

print('trend_range_per_DateTime')
print(trend_range_per_DateTime)
print()

print('trend_range_per_Seconds')
print(trend_range_per_Seconds)

#-----------------------------------------------------------------
#Categorize data based on trend ranges
#-----------------------------------------------------------------
orders['Trend'] = pd.cut(orders.Ticket, trend_range_per_order_tickets, labels=trend_labels).astype('category')
print(orders.groupby('Trend')[['DateTime', 'Ticket']].count())

history['Trend'] = pd.cut(history.Seconds, trend_range_per_Seconds, labels=trend_labels).astype('category')
print(history.groupby('Trend')[['DateTime', 'Close']].count())

indicator['Trend'] = pd.cut(indicator.Seconds, trend_range_per_Seconds, labels=trend_labels).astype('category')
print(indicator.groupby('Trend')['DateTime'].count())

#-----------------------------------------------------------------
# pickle data files
#-----------------------------------------------------------------
indicator.to_pickle('data/indicator_wTrends.pickle')
orders.to_pickle('data/orders_wTrends.pickle')
history.to_pickle('data/history_wTrends.pickle')
