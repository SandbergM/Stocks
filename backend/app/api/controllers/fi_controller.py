
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
from app.utils import CommonUtils


def get_insider_data( from_transactions_date, to_transactions_date = None, publisher = None ):
    
    rows = []

    today = datetime.today()

    to_transactions_date = to_transactions_date or str(today)
    publisher = publisher or ""

    page = 1
    
    while page:
        url = f""                                                                   \
            f"https://marknadssok.fi.se/Publiceringsklient/sv-SE/Search/Search?"    \
            f"SearchFunctionType=Insyn"                                             \
            f"&Utgivare={ publisher }"                                              \
            f"&PersonILedandeSt%C3%A4llningNamn="                                   \
            f"&Transaktionsdatum.From={ from_transactions_date }"                   \
            f"&Transaktionsdatum.To={ to_transactions_date }"                       \
            f"&Publiceringsdatum.From="                                             \
            f"&Publiceringsdatum.To="                                               \
            f"&button=search"                                                       \
            f"&Page={ page }"

        CommonUtils.log( f"Getting insider data page : { page }" )

        res = requests.get( url )
        doc = BeautifulSoup( res.text, 'html.parser' )

        columns = [ col.text for col in doc.find( "thead" ).find_all('th') ]

        res = doc.find( 'tbody' ).find_all( 'tr' )
        
        for row in res:
            rows.append({ key : str(val.text.strip()).replace('\xa0', '') for key, val in zip( columns, row.find_all( 'td' ) ) })

        page = page + 1 if len( res ) else 0
    
    return rows

def get_blanking_history( from_date = None, to_date = None ):

    from_date = from_date if from_date is not None else str(datetime.today())
    to_date = to_date if to_date is not None else str(datetime.today())

    url = "https://fi.se/sv/vara-register/blankningsregistret/GetHistFile/"
    df = pd.read_excel( url )

    columns = {
        "position_holder" : 'str',
        "name_of_issuer" : 'str',
        "isiin" : 'str',
        "position_in_percent" : 'float',
        "position_date" : 'str',
        "comment" : 'str'
    }

    df = df.iloc[5:]

    df.rename(columns={prev : new for prev, new in zip( df.columns, columns.keys())}, inplace=True)

    df['position_in_percent'] = df['position_in_percent'].apply(lambda x : str(x).replace('<0,5', '0.5'))
    df['position_in_percent'] = df['position_in_percent'].apply(lambda x : str(x).replace(',', '.'))
    df['comment'].fillna('', inplace=True)

    for key, val in columns.items():
        df[key] = df[key].astype( val )

    df = df.loc[(df['position_date'] >= from_date)&(df['position_date'] <= to_date)]

    return df.to_dict("records")