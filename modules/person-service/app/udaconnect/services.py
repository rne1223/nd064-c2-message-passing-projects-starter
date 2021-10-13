from typing import Dict, List

from app import db
from app.udaconnect.models import Person
from app.misc import log


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        log("GATHERING DETAILS AND INSERTING INTO DB")
        log(person)
        
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        log("PERSON CREATED IN DB WITH ID: " + new_person) 
        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
