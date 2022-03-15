from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from MissingSockDBQueries.MissingSock_database import Base
from flask_login import UserMixin
import json

from datetime import datetime, date

class Users(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), unique=True, nullable=False)
    name = Column(String(255),  nullable=True)
    surname = Column(String(255),  nullable=True)
    phone = Column(String(15),  nullable=True)
    farm_name = Column(String(255),  nullable=True)
    address_1 = Column(String(255),  nullable=True)
    address_2 = Column(String(255),  nullable=True)
    province = Column(String(20),  nullable=True)
    area = Column(String(255),  nullable=True)
    postal_code = Column(String(8),  nullable=True)
    gps_lat = Column(String(20), nullable=True)
    gps_long = Column(String(20), nullable=True) 

class Base_sync(UserMixin, Base):
    __tablename__ = 'base_sync'

    id = Column(Integer, primary_key=True)
    base_id = Column(String(255), nullable=False)
    tag_id = Column(String(255), nullable=False)
    gps_lat = Column(String(255), nullable=False)
    gps_long = Column(String(255), nullable=False)
    rssi = Column(String(255), nullable=False)
    sync_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=True)

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
    animal_reg_no = Column(String(255), nullable=True)
    asset_type = Column(String(255), nullable=True)
    group_name = Column(String(255), nullable=True)	
    date_of_birth = Column(Date, nullable=False, default=date.today)
    gender = Column(String(255), nullable=True)	
    breed_type = Column(String(255), nullable=True)
    father_id = Column(Integer, nullable=True)
    father_note = Column(String(255), nullable=True)
    mother_id = Column(Integer, nullable=True)
    mother_note = Column(String(255), nullable=True)
    users_id = Column(Integer, nullable=True)
    asset_breeding_id = Column(Integer, nullable=True)


class Asset_medical(UserMixin, Base):
    __tablename__ = 'asset_medical'

    id = Column(Integer, primary_key=True)	
    timestamp = Column(Date, nullable=False, default=date.today)
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
    start_date = Column(Date, nullable=False, default=date.today)
    end_date = Column(Date, nullable=True, default=date.today)
    twin_number	= Column(String(255), nullable=True)
    pregnant = Column(String(255), nullable=True)
    asset_registry_father_id = Column(Integer, nullable=True)
    asset_registry_mother_id = Column(Integer, nullable=True)
    users_id = Column(Integer, nullable=True)
    notes = Column(String(255), nullable=True)
  

class Asset_offspring(UserMixin, Base):
    __tablename__ = 'asset_offspring'

    id = Column(Integer, primary_key=True)	
    timestamp = Column(Date, nullable=False, default=date.today)
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
    timestamp = Column(Date, nullable=False, default=date.today)
    quantity = Column(Float	, nullable=False)	
    measurement = Column(String(255), nullable=False)
    note = Column(String(255), nullable=True)
    users_id = Column(Integer, nullable=True)

class Tag_current(UserMixin, Base):
    __tablename__ = 'tag_current'

    id = Column(Integer, primary_key=True)	
    gps_lat = Column(String(20), nullable=False)
    gps_long = Column(String(20), nullable=False)
    timestamp = Column(Date, nullable=True)
    base_station_id = Column(Integer, nullable=True)

class Tag_hist(UserMixin, Base):
    __tablename__ = 'tag_hist'

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, nullable=True)	
    gps_lat = Column(String(20), nullable=False)
    gps_long = Column(String(20), nullable=False)
    timestamp = Column(Date, nullable=True)
    base_station_id = Column(Integer, nullable=True)

class Base_station_current(UserMixin, Base):
    __tablename__ = 'base_station_current'

    id = Column(Integer, primary_key=True)	
    gps_lat = Column(String(20), nullable=False)
    gps_long = Column(String(20), nullable=False)
    timestamp = Column(DateTime, nullable=True)

class Base_station_hist(UserMixin, Base):
    __tablename__ = 'base_station_hist'

    id = Column(Integer, primary_key=True)	
    base_id = Column(Integer, nullable=False)
    gps_lat = Column(String(20), nullable=False)
    gps_long = Column(String(20), nullable=False)
    timestamp = Column(DateTime, nullable=True)

 
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

def sql_result_column_list_to_dict(my_col_list, sql_result):
    result = []
    for row in sql_result:
        dict_item = {}
        counter=0

        for value in row :
            
            dict_item[my_col_list[counter]] = value 
            counter += 1
        
        result.append(dict_item)

    return result

def row2dict(row):
    return {
        # cuts out foreignkey
        c.name: str(getattr(row, c.name))
        for c in row.__table__.columns
    }   
