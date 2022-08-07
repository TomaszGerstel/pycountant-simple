from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///"+os.path.join(BASE_DIR, 'site.db')

Base = declarative_base()
engine = create_engine(connection_string, echo=True)

Session = sessionmaker()
