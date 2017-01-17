from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


def configure_db(
    *,
    user='',
    password='',
    host='localhost',
    database='',
    charset='utf8mb4',
    create_tables=False,
    debug=False
) -> sessionmaker:
    connection_string = (
        'mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}'.format(
            user=user,
            password=password,
            host=host,
            database=database,
            charset=charset
        )
    )
    engine = create_engine(
        connection_string,
        echo=debug,
        echo_pool=debug
    )
    if create_tables:
        Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
