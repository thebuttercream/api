from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional, List
from ..models.schemas.person import PersonUpdate, PersonBase, PersonResponse


def create_person(db: Collection, person: PersonBase) -> PersonResponse:
    person_dict = person.model_dump()
    result = db["person"].insert_one(person_dict)
    return PersonResponse(**{**person_dict, "id": str(result.inserted_id)})


def get_person(db: Collection, person_id: str) -> Optional[PersonResponse]:
    person_data = db["person"].find_one({"_id": ObjectId(person_id)})
    if person_data:
        return PersonResponse(**{**person_data, "id": str(person_data["_id"])})
    return None


def get_all_person(db: Collection) -> List[PersonResponse]:
    people = list(db["person"].find())
    return [PersonResponse(**{**person, "id": str(person["_id"])}) for person in people]


def update_person(db: Collection, person_id: str, person: PersonUpdate) -> Optional[PersonResponse]:
    update_data = person.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data.pop('password')
    result = db["person"].update_one({"_id": ObjectId(person_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return get_person(db, person_id)


def delete_person(db: Collection, person_id: str) -> bool:
    result = db["person"].delete_one({"_id": ObjectId(person_id)})
    return result.deleted_count > 0
