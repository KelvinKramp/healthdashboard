import os
from datetime import date
from datetime import datetime as dt

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(ROOT_DIR, "config", ".env")

if os.path.isfile(os.path.join(ROOT_DIR,"local")):
    min_date = date(2021, 1, 1)
    max_date = dt.now().date()
else:
    min_date = date(2021, 12, 10)
    max_date = date(2021, 12, 23)

