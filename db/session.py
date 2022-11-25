from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os

from sqlalchemy_utils import database_exists, create_database

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# connection_string = "sqlite:///" + os.path.join(BASE_DIR, "site.db")

user = 'root'
password = 'root'
host = '127.0.0.1'
port = 3306
database = 'py-countant'

Base = declarative_base()

engine = create_engine(
                    url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}"
                    .format(user, password, host, port, database),
                    echo=True
                    )
if not database_exists(engine.url):
    create_database(engine.url)

# engine = create_engine(connection_string, echo=True, connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)
