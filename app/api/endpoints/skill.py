from typing import List
from pymongo.collection import Collection
from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.models.schemas.skill import SkillResponse, SkillUpdate, SkillRequest
from app.services.skill import create_skill, get_skill, get_all_skills, update_skill, delete_skill

router = APIRouter()


@router.post("/skill", response_model=SkillResponse)
def create_skill_route(skill: SkillRequest, db: Collection = Depends(get_db)):
    return create_skill(db, skill)


@router.get("/skill/{skill_id}", response_model=SkillResponse)
def get_skill_route(skill_id: str, db: Collection = Depends(get_db)):
    skill = get_skill(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill Not Found!!!")
    return skill


@router.get("/skill", response_model=List[SkillResponse])
def get_all_skills_route(db: Collection = Depends(get_db)):
    return get_all_skills(db)


@router.put("/skill/{skill_id}", response_model=SkillResponse)
def update_skill_route(skill_id: str, skill: SkillUpdate, db: Collection = Depends(get_db)):
    updated_skill = update_skill(db, skill_id, skill)
    if not updated_skill:
        raise HTTPException(status_code=404, detail="Skill Not Found!!!")
    return updated_skill


@router.delete("/skill/{skill_id}", response_model=bool)
def delete_skill_route(skill_id: str, db: Collection = Depends(get_db)):
    success = delete_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill Not Found!!!")
    return success
