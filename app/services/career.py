from uuid import uuid4
from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional, List
from ..models.schemas.career import CareerRequest, CareerResponse, CareerUpdate


def create_career(db: Collection, career: CareerRequest) -> CareerResponse:
    career_id = uuid4()
    career_dict = career.model_dump()
    career_dict['id'] = str(career_id)

    career_dict = {k: v for k, v in career_dict.items() if v is not None}

    result = db["career"].insert_one(career_dict)
    return CareerResponse(**{**career_dict, "id": str(result.inserted_id)})


def get_career(db: Collection, career_id: str) -> Optional[CareerResponse]:
    career_data = db["career"].find_one({"_id": ObjectId(career_id)})
    if career_data:
        return CareerResponse(**{**career_data, "id": str(career_data["_id"])})
    return None


def get_all_careers(db: Collection) -> List[CareerResponse]:
    careers = list(db["career"].find())
    return [CareerResponse(**{**career, "id": str(career["_id"])}) for career in careers]


def update_career(db: Collection, career_id: str, career: CareerUpdate) -> Optional[CareerResponse]:
    update_data = career.model_dump(exclude_unset=True)
    result = db["career"].update_one({"_id": ObjectId(career_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return get_career(db, career_id)


def delete_career(db: Collection, career_id: str) -> bool:
    result = db["career"].delete_one({"_id": ObjectId(career_id)})
    return result.deleted_count > 0
