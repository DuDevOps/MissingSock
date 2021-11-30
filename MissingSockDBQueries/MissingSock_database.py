from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import mysql
import pymysql



# app.config['SECRET_KEY'] = 'secret-key-goes-here'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{data_base}'
# app.config['SQLALCHEMY_POOL_SIZE'] = 50

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

host="192.168.0.116"
user="iodynami_script1"
password="koosK##S"
data_base="missingsock"

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{data_base}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import MissingSock_orm_models
    Base.metadata.create_all(bind=engine)