import os
from datetime import datetime, timedelta
from typing import Dict, List
from dotenv import load_dotenv

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text

from models import Person, Location, Connection

from log import log


load_dotenv()

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


Session = sessionmaker(bind=engine)
session = Session()

class Connections:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:

        log("FINDING CONNECTIONS")

        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """

        locations: List = session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        # Cache all users in memory for quick lookup
        # person_map: Dict[str, Person] = {person['id']: person for person in PersonService.retrieve_all()}
        person_map: Dict[str, Person] = {str(person.id): {"id" : person.id,
                                                    "first_name" : person.first_name,
                                                    "last_name" : person.last_name,
                                                    "company_name" : person.company_name}
                                            for person in session.query(Person)}
        result = person_map
        
        # log(f"Person map: { person_map }")
        # log(f"Locations: { locations } ")


        # Prepare arguments for queries
        # data = []
        # for location in locations:
        #     data.append(
        #         {
        #             "person_id": person_id,
        #             "longitude": location.longitude,
        #             "latitude": location.latitude,
        #             "meters": meters,
        #             "start_date": start_date.strftime("%Y-%m-%d"),
        #             "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
        #         }
        #     )

        # query = text(
        # """
        # SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        # FROM    location
        # WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        # AND     person_id != :person_id
        # AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        # AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        # """
        # )
        # result: List[Dict] = []
        # for line in tuple(data):
        #     for (
        #         exposed_person_id,
        #         location_id,
        #         exposed_lat,
        #         exposed_long,
        #         exposed_time,
        #     ) in session.execute(query, line):

        #         locations = { "location_id" : location_id, 
        #                     "person_id":exposed_person_id, 
        #                     "time":exposed_time,
        #                     "lat":exposed_lat,
        #                     "lon":exposed_long 
        #         }

                # result.append( {"person": person_map[exposed_person_id], 
                #                 "locations": locations})
        
        # log(result)
        return result