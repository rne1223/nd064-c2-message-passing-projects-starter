import os
import psycopg2
from dotenv import load_dotenv
from log import log
from models import Location
from schemas import LocationSchema

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from geoalchemy2.functions import ST_AsText, ST_Point
from typing import Dict

load_dotenv()

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

Session = sessionmaker(bind=engine)
session = Session()

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

def save_to_db(location):

    log("SAVING LOCATION:")

    validation_results: Dict = LocationSchema().validate(location)
    if validation_results:
        log(f"Unexpected data format in payload: {validation_results}")
        raise Exception(f"Invalid payload: {validation_results}")

    new_location = Location()
    new_location.person_id = location["person_id"]
    new_location.creation_time = location["creation_time"]
    new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
    session.add(new_location)
    session.commit()

    return new_location