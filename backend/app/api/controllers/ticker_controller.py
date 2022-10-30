
from app.api.services.ticker_service import get_ticker_data

import pandas as pd
import numpy as np
import datetime
import json
import math
from datetime import timedelta
from datetime import datetime

from sklearn.preprocessing import MinMaxScaler

from tensorflow import keras
from keras.layers import Dense, LSTM
from keras.models import Sequential, load_model

from ...__data import DbHandler

def ticker_search( company_name_search = None ):
    if company_name_search is not None:
        return DbHandler.select_query( f"""SELECT ticker, unix, company_name, country FROM tickers WHERE company_name LIKE ? ORDER BY ticker ASC LIMIT 25""", ( f"%{company_name_search}%", ) )
    else:
        return DbHandler.select_query( f"""SELECT ticker, unix, company_name, country FROM tickers ORDER BY ticker ASC LIMIT 25""" )
    
def get_ticker_historical_data( ticker, company_name, start, end, interval = '1d' ):

    try:    

        # Full url
        url = f''\
        f'https://query1.finance.yahoo.com/v7/finance/download/{ ticker }'\
        f'?period1={ int(start) }'\
        f'&period2={ int(end) }'\
        f'&interval={ interval }'\
        f'&events=history'\
        f'&includeAdjustedClose=true'

        # Get CSV
        res                 = pd.read_csv( url )

        # Fix col names
        res.columns         = [ col.replace(' ', '_').replace( '*', '' ).lower().strip() for col in res.columns ]
        
        # Add ticker and company_name as columns
        res                 = res.reindex([ 'ticker', 'company_name', *res.columns.tolist() ], axis = 1)
        res['ticker']       = ticker
        res['company_name'] = company_name

        # Remove prev saved days ( If found )
        start_dt            = datetime.fromtimestamp(int( start ))
        res['date']         = pd.to_datetime(res['date'], format="%Y-%m-%d")
        res.drop(res[(res['date'] <= start_dt )].index, inplace=True)
        
        # Some 'volume's come as float for some reason
        res.dropna( inplace=True )
        res['volume']       = res['volume'].astype(np.int64)
        
        return res

    except Exception as e :
        print(e)
        return pd.DataFrame()

def get_ticker_prediction( ticker, prediction_days = 7, start = '2000-01-01', end = '2022-08-27', epochs = 30 ):

    
    ticker_data = get_ticker_data( ticker, start, end )
    ticker_data['date'] = ticker_data['date'].dt.date

    max_ticker_data = ticker_data['date'].max()

    data = ticker_data.filter(['close'])
    dataset = data.values

    traning_data_len = math.ceil( len(dataset) * 0.8 )

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data[0:traning_data_len, : ]

    x_train = []
    y_train = []

    for i in range( prediction_days, len( train_data ) ):
        x_train.append(train_data[i-prediction_days:i, 0])
        y_train.append( train_data[i, 0] )

    x_train, y_train = np.array( x_train ), np.array( y_train )

    x_train = np.reshape( x_train, ( x_train.shape[0], x_train.shape[1], 1 ))

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape = ( x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False ))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile( optimizer = 'adam', loss = 'mean_squared_error' )

    model.fit( x_train, y_train, batch_size = 50, epochs = epochs )

    test_data = scaled_data[traning_data_len - prediction_days: , : ]
    
    x_test = []

    for i in range( prediction_days, len(test_data) ):
        x_test.append( test_data[i-prediction_days:i, 0] )

    x_test = np.array( x_test )
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    predictions = model.predict( x_test )
    predictions = scaler.inverse_transform( predictions )

    ticker_data['date'] = ticker_data['date'].astype( str )
    res = [ dict( row ) for idx, row in ticker_data[['ticker', 'date', 'close']].iterrows() ]

    for pred in predictions:

        max_ticker_data += timedelta(days=1)

        weekend_days = {
            6 : 2,
            7 : 1
        }

        if max_ticker_data.isoweekday() in weekend_days.keys():
            max_ticker_data += timedelta(days= weekend_days.get( max_ticker_data.isoweekday() ) )


        res.append({
            'ticker' : ticker,
            'date' : max_ticker_data.strftime('%Y-%m-%d'),
            'close' : float( pred[0] ),
            'predicted' : True
        })

    def customSort( k ):
        return k['date']

    res.sort( key=customSort, reverse=False )

    return json.dumps( res )
