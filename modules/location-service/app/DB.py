import os 
import psycopg2
from dotenv import load_dotenv
from log import log

load_dotenv()

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

# db = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# def get_db_connection():
#     connection = db.connect() 

def _db_connect():
    log("GRPC CONNECTING TO DB")
    db_conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    log("GRPC CONNECTED")
    return db_conn

def save_to_db(location_data):

    log("SAVING LOCATION:")
    conn = _db_connect()
    cursor = conn.cursor()
    # person_id = int(location_data["person_id"])
    # latitude = float(location_data["latitude"])
    # longitude = float(location_data["longitude"])
    person_id = 1 
    latitude = "testing Lat" 
    longitude = "testing long" 
    # sql = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, latitude, longitude)
    # cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

    log("LOCATION SAVED")

def getLocById(id):

    log("GETTING LOCATION BY ID FROM DB:")
    conn = _db_connect()
    cursor = conn.cursor()
    sql = f"SELECT ST_AsText(*) FROM LOCATION WHERE id={id}"
    data = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

    return data