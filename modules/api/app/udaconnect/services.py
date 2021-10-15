import logging
from time import sleep
from datetime import datetime, timedelta
from typing import Dict, List
import requests
from app import db
from app.misc import log
from app.location_grpc import getLocation

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaProducer, KafkaConsumer
from json import dumps, load, loads

from multiprocessing import Process

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

serviceUrl = "http://udaconnect-person-service:5001/api/persons"

# Set up a Kafka producer
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                        value_serializer=lambda x: dumps(x).encode('utf-8'),
                        api_version=(0,10,1))

# Set up a Kafka consumer 
TOPIC_NAME = 'con'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='api-consumer',
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     api_version=(0,10,1))

class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        ''' Find all contacts giving a person_id, an starting and end date, as well as a distance.
            For the connection service we are using Kafka for communications between services '''

        
        log("FINDING CONNECTIONS")

        # Sending data to Connection Service through Kafka
        dts = {"person_id": str( person_id ),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")}
        producer.send("items",value=dts)

        # Getting data from Connection Service through Kafka
        person_map: Dict[str, Person] = []
        for message in consumer: 
            persons = message.value
            person_map = loads(persons.replace("'",'"'))
            break

        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )
        query = text(
        """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)

                result.append(
                    Connection(
                        person=person_map[str(exposed_person_id)], location=location,
                    )
                )

        return result


class LocationService:
    @staticmethod
    def retrieve_all() -> Location:
        ''' Retrive all locations using GRPC as the communication method'''
        response = getLocation()
        return response

    @staticmethod
    def retrieve(location_id) -> Location:
        ''' Retrive a single location by id using GRPC as the communication method'''

        # using grpc to call the Location service
        location = getLocation(location_id)
        log("LOCATION RETRIEVED FROM DB")
        log(location)
        return location


    @staticmethod
    def create(location: Dict) -> Location:
        ''' Create a new location in DB using GRPC as the communication method'''
        new_location = getLocation(location)
        return new_location


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        log("GATHERING DETAILS AND INSERTING INTO DB")
        log(person)
        response = requests.post(f"{serviceUrl}", json=person)
        log(response.json())

        if(response.status_code == 200):
            new_person = response.json()
            return new_person 
        else:
            return {"error": response.status_code}

    @staticmethod
    def retrieve(person_id: int) -> Person:
        # Use person-service to retrieve a person by id
        response = requests.get(f"{serviceUrl}/{person_id}")

        if(response.status_code == 200):
            person = response.json()
            return person
        else:
            return {"error":response.status_code}

    @staticmethod
    def retrieve_all() -> List[Person]:
        # Use person-service to retrieve all persons from DB
        response = requests.get(f"{serviceUrl}")

        if(response.status_code == 200):
            persons = response.json()
            return persons
        else:
            return {"error":response.status_code}
