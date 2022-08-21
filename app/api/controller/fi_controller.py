from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

def get_insider_data( **args ):

    rows = []

    today = datetime.today()

    from_transactions_date = args.get( "from_transactions_date" ) or str(today)
    to_transactions_date = args.get( "to_transactions_date" ) or str(today)
    publisher = args.get( "publisher" ) or ""


    page = args.get( "page" ) or 1
    
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

        res = requests.get( url )
        doc = BeautifulSoup( res.text, 'html.parser' )

        columns = [ col.text for col in doc.find( "thead" ).find_all('th') ]

        res = doc.find( 'tbody' ).find_all( 'tr' )
        
        for row in res:
            rows.append({ key : str(val.text.strip()).replace('\xa0', '') for key, val in zip( columns, row.find_all( 'td' ) ) })

        page = page + 1 if len( res ) else 0
    
    return rows

def get_blanking_history( **args ):

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

    df.rename(columns={
        prev : new for prev, new in zip( df.columns, columns.keys() )
    }, inplace=True)

    df['position_in_percent'] = df['position_in_percent'].str.replace('<0,5', '0.5')
    df['position_in_percent'] = df['position_in_percent'].str.replace(',', '.')

    df['comment'].fillna('', inplace=True)
    df['position_in_percent'].dropna( inplace=True )

    for key, val in columns.items():
        df[key] = df[key].astype( val )

    if args.get('return_type') == "json":
        return df.to_json(orient='records')

    else:
        return df