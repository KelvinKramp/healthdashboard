import dash
import dash_bootstrap_components as dbc
from definitions import ROOT_DIR
import os

# START APP
app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                assets_folder=os.path.join(ROOT_DIR, 'assets'),
                external_stylesheets=[dbc.themes.FLATLY])
server = app.server


# CONFIGURE DATABASE
# IMPORT DATABASE_URL
# from db_connection.create_engine import DATABASE_URL

# from flask_sqlalchemy import SQLAlchemy
# import configparser
# import os

# config = configparser.ConfigParser()
# server.config.update(
#     SECRET_KEY=os.urandom(12),
#     SQLALCHEMY_DATABASE_URI=DATABASE_URL,
#     SQLALCHEMY_TRACK_MODIFICATIONS=False
# )
# db = SQLAlchemy(server)
# db.init_app(server)




