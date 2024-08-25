from uuid import uuid4
from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional, List
from ..models.schemas.skill import SkillRequest, SkillResponse, SkillUpdate


def create_skill(db: Collection, skill: SkillRequest) -> SkillResponse:
    skill_id = uuid4()
    skill_dict = skill.model_dump()
    skill_dict['id'] = str(skill_id)

    skill_dict = {k: v for k, v in skill_dict.items() if v is not None}

    result = db["skill"].insert_one(skill_dict)
    return SkillResponse(**{**skill_dict, "id": str(result.inserted_id)})


def get_skill(db: Collection, skill_id: str) -> Optional[SkillResponse]:
    skill_data = db["skill"].find_one({"_id": ObjectId(skill_id)})
    if skill_data:
        return SkillResponse(**{**skill_data, "id": str(skill_data["_id"])})
    return None


def get_all_skills(db: Collection) -> List[SkillResponse]:
    skills = list(db["skill"].find())
    return [SkillResponse(**{**skill, "id": str(skill["_id"])}) for skill in skills]


def update_skill(db: Collection, skill_id: str, skill: SkillUpdate) -> Optional[SkillResponse]:
    existing_skill = get_skill(db, skill_id)
    if not existing_skill:
        return None

    update_data = skill.model_dump(exclude_unset=True)
    result = db["skill"].update_one({"_id": ObjectId(skill_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None

    return get_skill(db, skill_id)


def delete_skill(db: Collection, skill_id: str) -> bool:
    result = db["skill"].delete_one({"_id": ObjectId(skill_id)})
    return result.deleted_count > 0
