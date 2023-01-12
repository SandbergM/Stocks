import datetime
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta

def log( msg ):
    """
    @param String msg
    """
    print( f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}     -  * {msg}" )


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

def get_rsi(values):
    
    if len(values) == 0:
        return None

    loss = 1
    gain = 1
    
    for idx in range(1, len(values), 1):

        prev = values[idx-1]
        curr = values[idx]

        if curr > prev:
            gain += curr - prev

        if curr < prev:
            loss += prev - curr


    rs = (gain/len(values)) / (loss/len(values))

    return 100 - (100 / (1+rs))

def float_round(val, round_to):
    if val is not None:
        return round(val, round_to)
    return val

def generate_date(interval_type, interval_length):

    today_date = datetime.now()
    last_monday = today_date - relativedelta(days=-today_date.weekday(), weeks=1)

    if interval_type == "day":
        return last_monday - relativedelta(days=int(interval_length))

    if interval_type == "week":
        return last_monday - relativedelta(weeks=int(interval_length))

    if interval_type == "month":
        return last_monday - relativedelta(months=int(interval_length))

    if interval_type == "year":
        return last_monday - relativedelta(years=int(interval_length))
    
    return last_monday