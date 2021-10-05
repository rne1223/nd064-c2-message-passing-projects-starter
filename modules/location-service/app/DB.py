import os
import psycopg2
from dotenv import load_dotenv
from log import log
from shapely import geometry, wkb

from sqlalchemy import create_engine

# from sqlalchemy.orm.session import sessionmaker
# from models import Location
# from schemas import LocationSchema
# from geoalchemy2.functions import ST_AsText, ST_Point
# # from sqlalchemy.sql import text
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, query, sessionmaker

load_dotenv()

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def _db_connect():
    log("GRPC CONNECTING TO DB")
    db_conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    log("GRPC CONNECTED TO DB")
    return db_conn

def getLocById(id=None):

    conn = _db_connect()
    cursor = conn.cursor()
    
    if(id):
        log("GETTING LOCATION BY ID FROM DB:")
        sql = f"SELECT * FROM location WHERE id={int(id)}"
    else:
        log("GETTING ALL LOCATIONS FROM DB:")
        sql = f"SELECT * FROM location"

    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    return data

# def save_to_db(location_data):

#     log("SAVING LOCATION:")
#     conn = _db_connect()
#     cursor = conn.cursor()
#     # person_id = int(location_data["person_id"])
#     # latitude = float(location_data["latitude"])
#     # longitude = float(location_data["longitude"])
#     person_id = 1 
#     latitude = "testing Lat" 
#     longitude = "testing long" 
#     # sql = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, latitude, longitude)
#     # cursor.execute(sql)
#     conn.commit()
#     cursor.close()
#     conn.close()

#     log("LOCATION SAVED")
