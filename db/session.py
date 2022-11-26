
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from pycountant.model import Base

# Base = declarative_base()

# for connection with mysql db
user = 'root'
password = 'root'
# host name for working on docker
host = 'mysql'
# host = 'localhost'
port = '3306'
database = 'py-countant'
# mysql engine
engine = create_engine(
                    url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}"
                    .format(user, password, host, port, database),
                    echo=True
                    )

Session = sessionmaker(bind=engine)

# for connection with sqlite db
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# connection_string = "sqlite:///" + os.path.join(BASE_DIR, "site.db")
# engine = create_engine(connection_string, echo=True, connect_args={"check_same_thread": False})

if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(engine)

