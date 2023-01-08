import datetime
import numpy as np

def log( msg ):
    """
    @param String msg
    """
    print( f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}     -  * {msg}" )


def get_weighted_moving_average(values):

    if len(values) == 0:
        return None

    weight_factor = sum([idx + 1 for idx in range(len(values))])
    weight = 1
    weighted_sum = 0

    for val in values:
        weighted_sum = (weighted_sum + (float(val) * (weight / weight_factor)))
        weight += 1

    return weighted_sum

def get_sma(prices, rate):
    return prices.rolling(rate).mean()

def get_bollinger_bands(prices, rate, diviation):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * diviation
    bollinger_down = sma - std * diviation

    bollinger_up = bollinger_up.replace(np.nan, None)
    bollinger_down = bollinger_down.replace(np.nan, None)

    return bollinger_up.values.tolist(), bollinger_down.values.tolist()