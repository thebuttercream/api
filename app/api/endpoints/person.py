from typing import List

from pymongo.collection import Collection

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.models.schemas import PersonResponse, PersonBase, PersonUpdate
from app.services.person_service import create_person, get_person, get_all_person, update_person, delete_person

router = APIRouter()


@router.post("/person", response_model=PersonResponse)
def create_person_route(person: PersonBase, db: Collection = Depends(get_db)):
    return create_person(db, person)


@router.get("/person/{person_id}", response_model=PersonResponse)
def get_person_route(person_id: str, db: Collection = Depends(get_db)):
    person = get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person Not Found!!!")
    return person


@router.get("/person", response_model=List[PersonResponse])
def get_all_person_route(db: Collection = Depends(get_db)):
    return get_all_person(db)


@router.put("/person/{person_id}", response_model=PersonResponse)
def update_person_route(person_id: str, person: PersonUpdate, db: Collection = Depends(get_db)):
    updated_person = update_person(db, person_id, person)
    if not updated_person:
        raise HTTPException(status_code=404, detail="Person Not Found!!!")
    return updated_person


@router.delete("/person/{person_id}", response_model=bool)
def delete_person_route(person_id: str, db: Collection = Depends(get_db)):
    success = delete_person(db, person_id)
    if not success:
        raise HTTPException(status_code=404, detail="Person Not Found!!!")
    return success
