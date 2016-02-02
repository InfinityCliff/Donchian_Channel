import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as DT
print('system: ', sys.version)
print('numpy: ', np.__version__)
print('panda: ', pd.__version__)

# read in Indicator data into dataframe
parser = lambda date: pd.datetime.strptime(date, '%Y.%m.%d %H:%M:%S')
df_Ind = pd.read_csv('data/150001_Indicators.csv', parse_dates=[0], date_parser=parser)

# rename 'Date' column to 'DateTime' and split apart
df_Ind.rename(columns={'Date': 'DateTime'}, inplace=True)
temp = pd.DatetimeIndex(df_Ind['DateTime'])
df_Ind['Date'] = temp.date
df_Ind['Time'] = temp.time

# re-arrange to put 'Date' and 'Time' up front behind 'DateTime'
cols = df_Ind.columns.tolist()
cols = cols[0:1] + cols[-2:] + cols[1:-2]
df_Ind = df_Ind[cols]
df_Ind.head()

# read in order data
df_ord = pd.read_csv('data/150001_Orders.csv', parse_dates=[1], date_parser=parser)

# rename 'Date' column to 'DateTime' and split apart
df_ord.rename(columns={'Open Time': 'DateTime'}, inplace=True)
temp = pd.DatetimeIndex(df_ord['DateTime'])
df_ord['Date'] = temp.date
df_ord['Time'] = temp.time

# re-arrange to put 'Date' and 'Time' up front behind 'DateTime'
cols = df_ord.columns.tolist()
cols = cols[1:2] + cols[-2:] + cols[0:1] + cols[2:-2]
df_ord = df_ord[cols]


def rolling_profit_count(dataframe):  # function returns sum of count of number of profit (+1) and loss trades (-1)
    count = 0
    for profit in dataframe:
        if profit >= 0:
            count = count + 1
        else:
            count = count -1
    return count

# Add Rolling stats to Order DF
window = 15
df_ord['Roll_Profit_Count'] = pd.rolling_apply(df_ord['Profit'], window, rolling_profit_count,1)
df_ord['Roll_Mean'] = pd.rolling_mean(df_ord['Profit'], window)
df_ord['Roll_std'] = pd.rolling_std(df_ord['Profit'], window)
df_ord['Roll_var'] = pd.rolling_var(df_ord['Profit'], window)


# Create Trend Ranges, based on visual inspection of previous graph, and add Trends to Order dataframe
trend_range = [0, 6, 33, 60, 77, 86, 150, 171, 207, 222, 271, 314, 331, 348]
trend_labels = ['UP1', 'FLAT1', 'DOWN1', 'UP2', 'DOWN2', 'FLAT2', 'DOWN3', 'UP3', 'DOWN4', 'UP4', 
                'DOWN5', 'UP6', 'FLAT3']

df_ord['Trend'] = pd.cut(df_ord.Ticket, trend_range, labels=trend_labels).astype('category')


# Order Dataframe with Trends added
df_ord[['DateTime', 'Ticket', 'Profit', 'Trend', 'Roll_Profit_Count', 'Roll_Mean', 'Roll_std']].head()


# function to convert 'DateTime' to seconds
seconds = lambda x: (x - DT.datetime(1970, 1, 1)).total_seconds()

# Convert Date time in Order DF to seconds and pull that Series out
df_ord['DateTime_sec'] = df_ord['DateTime'].apply(seconds)


# pull 'Times' of trend range changes from order dataframe
# i.e. if 'Ticket' is in trend_range list, return the 'DateTime'
trend_range_DT = df_ord[df_ord['Ticket'].isin(trend_range)]['DateTime']
trend_range_DT_sec = df_ord[df_ord['Ticket'].isin(trend_range)]['DateTime_sec']


# Add the 'first ticket time' to the Series
zerotime = int(df_ord['DateTime_sec'][0])
trend_range_DT_sec = trend_range_DT_sec.append(pd.Series([zerotime])).sort_values(ascending=True)
zerotime = df_ord['DateTime'][0]
trend_range_DT = trend_range_DT.append(pd.Series([zerotime])).sort_values(ascending=True)

# Convert Date time in Indicator DF to seconds and pull that Series out
df_Ind['DateTime_sec'] = df_Ind['DateTime'].apply(seconds)


df_Ind['Trend'] = pd.cut(df_Ind.DateTime_sec, trend_range_DT_sec, labels=trend_labels).astype('category')

# DOWN1_BBAND = df_Ind[(df_Ind.Trend == 'DOWN1')][['DateTime', 'BBAND(10)', 'BBAND(50)', 'BBAND(100)', 'BBAND(150)', 'BBAND(200)']]
# DOWN1_MACD_MAIN = df_Ind[(df_Ind.Trend == 'DOWN1')][['DateTime', 'MACD(2) MAIN', 'MACD(10) MAIN', 'MACD(20) MAIN']]
# DOWN1_MACD_SIGNAL = df_Ind[(df_Ind.Trend == 'DOWN1')][['DateTime', 'MACD(2) SIGNAL', 'MACD(10) SIGNAL', 'MACD(20) SIGNAL']]


# plt.plot(list(df_Ind['DateTime'][df_Ind.Trend == 'DOWN1']), df_Ind[(df_Ind.Trend == 'DOWN1')][['BBAND(10)', 'BBAND(50)', 'BBAND(100)']])
# 
# plt.show()


# DOWN1_BBAND.set_index('DateTime', inplace=True)
# DOWN1_MACD_MAIN.set_index('DateTime', inplace=True)
# DOWN1_MACD_SIGNAL.set_index('DateTime', inplace=True)

# Ceate data from from Indicator data frame to use for evaluation
study = df_Ind.loc[:, ('DateTime', 'Trend', 'BBAND(100)', 'MACD(12) MAIN', 'MACD(2) SIGNAL', 'MACD(10) SIGNAL', 'MACD(20) SIGNAL')]

# add stats to study data frame
study['bband100_std'] = pd.rolling_std(study['BBAND(100)'], 7)
study['macd12main_std'] = pd.rolling_std(study['MACD(12) MAIN'], 7)
study['macd2signal_std'] = pd.rolling_std(study['MACD(2) SIGNAL'], 7)
study['macd10signal_std'] = pd.rolling_std(study['MACD(10) SIGNAL'], 7)
study['macd20signal_std'] = pd.rolling_std(study['MACD(20) SIGNAL'], 7)


#study.set_index('DateTime', inplace=True)


# study['MACD(12) MAIN'].plot()
# plt.show()


# define filters for trend periods
up1 = (study['Trend'] == 'UP1')
flat1 = (study['Trend'] == 'FLAT1')
down1 = (study['Trend'] == 'DOWN1')
up2 = (study['Trend'] == 'UP2')
down2 = (study['Trend'] == 'DOWN2')
flat2 = (study['Trend'] == 'FLAT2')
down3 = (study['Trend'] == 'DOWN3')
up3 = (study['Trend'] == 'UP3')
down4 = (study['Trend'] == 'DOWN4')
up4 = (study['Trend'] == 'UP4')
down5 = (study['Trend'] == 'DOWN5')
up6 = (study['Trend'] == 'UP6')
flat3 = (study['Trend'] == 'FLAT3')


# xt = np.arange(lambda x: float(x), trend_range_DT)
# type(xt)
maxy = 0.0004
plt.subplot(2, 1, 1)
plt.title('MACD (12) Main - STD')
plt.plot(study[up1].set_index('DateTime')['macd12main_std'], 'b')
#study[down1].set_index('DateTime')['macd12main_std'].plot()
plt.ylabel('Period UP1')
plt.ylim(ymax=maxy)
# plt.xticks(np.arange(xt))

plt.subplot(2, 1, 2)
plt.plot(study[down1].set_index('DateTime')['macd12main_std'], 'g')
plt.ylabel('Period DOWN1')
plt.ylim(ymax=maxy)
plt.xlabel('Date')

plt.show()







