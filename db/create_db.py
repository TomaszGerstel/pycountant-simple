from db.session import engine
from pycountant.model import Base


def create_database_schema():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_database_schema()
