# IMPORT MODULES
from dash import html
from app.app import app


layout = html.Div([])

if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)