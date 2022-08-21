from app.api.routes.fi_routes import insider_data_route, blanking_history_route

def run_route( request ):
    print( request.path )
    path = request.path.replace( '/api/', '' )

    if path == 'fi/insider_data':
        return insider_data_route( request )

    if path == 'fi/blanking_history':
        return blanking_history_route( request )