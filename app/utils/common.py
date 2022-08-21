import datetime

def log( msg ):
    """
    @param String msg
    """
    curr_datetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print( f"     ###     [{curr_datetime}] { msg }" )