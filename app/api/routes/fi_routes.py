
from app.api.controller.fi_controller import get_insider_data
from app.api.controller.fi_controller import get_blanking_history


def insider_data_route( request ):
    return get_insider_data( **request.args ), 200

def blanking_history_route( request ):
    return get_blanking_history( **request.args ), 200