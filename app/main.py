#!/usr/bin/env python3

import connexion

from app import encoder

app = connexion.App(__name__, specification_dir = './swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'DWD-Proxy'})
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = 1, port = 8080)