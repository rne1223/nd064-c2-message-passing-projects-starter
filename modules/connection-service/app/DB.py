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

        person_map: Dict[str, Person] = {str(person.id): {"id" : person.id,
                                                    "first_name" : person.first_name,
                                                    "last_name" : person.last_name,
                                                    "company_name" : person.company_name}
                                            for person in session.query(Person)}
        result = person_map
        
        return result