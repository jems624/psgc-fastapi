import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from app.settings import settings

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)
Session = sessionmaker(autocommit=False, bind=engine)