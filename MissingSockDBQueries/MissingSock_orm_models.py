from sqlalchemy import Column, Integer, String, DateTime, Float
from MissingSockDBQueries.MissingSock_database import Base
from flask_login import UserMixin
import json

from datetime import datetime

class Users(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), unique=True, nullable=False)

class Base_station(UserMixin, Base):
    __tablename__ = 'base_station'

    id = Column(Integer, primary_key=True)
    sync_base_id = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=True)
    users_id = Column(Integer, nullable=True)

class Tag(UserMixin, Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    sync_tag_id = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=True)
    users_id = Column(Integer, nullable=True)

class Asset_registry(UserMixin, Base):
    __tablename__ = 'asset_registry'

    id = Column(Integer, primary_key=True)	
    tag_id = Column(Integer, nullable=True)
    asset_type = Column(String(255), nullable=True)
    asset_number = Column(String(255), nullable=True)	
    group_number = Column(String(255), nullable=True)	
    date_of_birth = Column(DateTime, nullable=False, default=datetime.utcnow)
    gender = Column(String(255), nullable=True)	
    breed_type = Column(String(255), nullable=True)
    father_id = Column(Integer, nullable=True)
    father_note = Column(String(255), nullable=True)
    mother_id = Column(Integer, nullable=True)
    mother_note = Column(String(255), nullable=True)
    users_id = Column(Integer, nullable=True)


class Asset_medical(UserMixin, Base):
    __tablename__ = 'asset_medical'

    id = Column(Integer, primary_key=True)	
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    reason = Column(String(255), nullable=True)	
    medicine = Column(String(255), nullable=True)
    dosage = Column(Float	, nullable=True)
    note = Column(String(255), nullable=True)
    asset_registry_id = Column(Integer,  nullable=False)
    users_id = Column(Integer, nullable=True)


class Asset_breeding(UserMixin, Base):
    __tablename__ = 'asset_breeding'

    id = Column(Integer, primary_key=True)	
    breeding_number = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True, default=datetime.utcnow)
    twin_number	= Column(String(255), nullable=True)
    pregnant = Column(Integer, nullable=True)
    asset_registry_father_id = Column(Integer, nullable=True)
    asset_registry_mother_id = Column(Integer, nullable=True)
    users_id = Column(Integer, nullable=True)
  

class Asset_offspring(UserMixin, Base):
    __tablename__ = 'asset_offspring'

    id = Column(Integer, primary_key=True)	
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    asset_father_id = Column(Integer, nullable=True)
    asset_mother_id = Column(Integer, nullable=True)
    asset_offspring_id = Column(Integer, nullable=True)
    asset_breeding_id = Column(Integer, nullable=True)
    users_id = Column(Integer, nullable=True)

class Asset_produce(UserMixin, Base):
    __tablename__ = 'asset_produce'

    id = Column(Integer, primary_key=True)	
    asset_registry_id = Column(Integer,  nullable=False)
    type = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    produce_yield = Column(Float	, nullable=False)	
    measurement = Column(String(255), nullable=False)
    note = Column(String(255), nullable=True)
    users_id = Column(Integer, nullable=True)

 
def sql_result_to_json(sql_result):
    result = [
           row2dict(report)
           for report in sql_result
    ]

    result_json = json.dumps(result)

    return result_json

def sql_result_to_dict(sql_result):
    result = [
           row2dict(row)
           for row in sql_result
    ]

    return result

def row2dict(row):
    return {
        # cuts out foreignkey
        c.name: str(getattr(row, c.name))
        for c in row.__table__.columns
    }   