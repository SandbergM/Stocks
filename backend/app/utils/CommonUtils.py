import datetime

def log( msg ):
    """
    @param String msg
    """
    print( f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}     -  * {msg}" )