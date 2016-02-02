import pandas as pd
import numpy as np

#-----------------------------------------------------------------
# Compute Simple Moving Average
#-----------------------------------------------------------------
def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

    
#-----------------------------------------------------------------
# Compute Exponential Moving Average
#-----------------------------------------------------------------
def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

    
#-----------------------------------------------------------------
#  compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
#  return value is emaslow, emafast, macd which are len(x) arrays
#-----------------------------------------------------------------
def computeMACD(x, slow=26, fast=12):
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow

#-----------------------------------------------------------------
#    The Rate-of-Change (ROC) indicator, a.k.a. Momentum, is a pure momentum
#    oscillator that measures the percent change in price from one period to the
#    next.
#    The plot forms an oscillator that fluctuates above and below the zero line
#    as the Rate-of-Change moves from positive to negative.
#    ROC signals include center line crossovers, divergences and
#    overbought-oversold readings. Identifying overbought or oversold extremes
#    comes natural to the Rate-of-Change oscillator.
#    It can be used to measure the ROC of any data series, such as price or
#    another indicator.
#    Also known as PROC when used with price.
#    ROC = [(Close - Close n periods ago) / (Close n periods ago)] * 100
#-----------------------------------------------------------------
def roc(prices, period=21):
    d = prices.diff(period - 1)
    rocs = (d / (prices - d)) * 100
    return rocs

def rsi(prices, n=14):
    # RSI = 100 - (100 / (1 + RS))
    # where RS = (Wilder-smoothed n-period average of gains / Wilder-smoothed n-period average of -losses)
    # Note that losses above should be positive values
    # Wilder-smoothing = ((previous smoothed avg * (n-1)) + current value to average) / n
    # For the very first "previous smoothed avg" (aka the seed value), we start with a straight average.
    # Therefore, our first RSI value will be for the n+2nd period:
    #     0: first delta is nan
    #     1:
    #     ...
    #     n: lookback period for first Wilder smoothing seed value
    #     n+1: first RSI

    # First, calculate the gain or loss from one price to the next. The first value is nan so replace with 0.
    deltas = (prices-prices.shift(1)).fillna(0)

    # Calculate the straight average seed values.
    # The first delta is always zero, so we will use a slice of the first n deltas starting at 1,
    # and filter only deltas > 0 to get gains and deltas < 0 to get losses
    avg_of_gains = deltas[1:n+1][deltas > 0].sum() / n
    avg_of_losses = -deltas[1:n+1][deltas < 0].sum() / n

    # Set up pd.Series container for RSI values
    rsi_series = pd.Series(0.0, deltas.index)

    # Now calculate RSI using the Wilder smoothing method, starting with n+1 delta.
    up = lambda x: x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in deltas[n+1:]:
        print(i)
        avg_of_gains = ((avg_of_gains * (n-1)) + up(d)) / n
        avg_of_losses = ((avg_of_losses * (n-1)) + down(d)) / n
        if avg_of_losses != 0:
            rs = avg_of_gains / avg_of_losses
            rsi_series[i] = 100 - (100 / (1 + rs))
        else:
            rsi_series[i] = 100
        i += 1

    return rsi_series