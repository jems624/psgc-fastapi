# import pandas as pd
# from app.data import geo_data
from app.db.session import Session as DBSession
from sqlalchemy.orm import Session


# def get_geo_data() -> pd.DataFrame:
#     return geo_data

def get_db() -> Session:
    db = DBSession()
    try:
        yield db
    finally:
        db.close()