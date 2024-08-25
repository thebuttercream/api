from typing import List

from pymongo.collection import Collection
from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.models.schemas.career import CareerResponse, CareerUpdate, CareerRequest
from app.services.career import create_career, get_career, get_all_careers, update_career, delete_career

router = APIRouter()


@router.post("/career", response_model=CareerResponse)
def create_career_route(career: CareerRequest, db: Collection = Depends(get_db)):
    return create_career(db, career)


@router.get("/career/{career_id}", response_model=CareerResponse)
def get_career_route(career_id: str, db: Collection = Depends(get_db)):
    career = get_career(db, career_id)
    if not career:
        raise HTTPException(status_code=404, detail="Career Not Found!!!")
    return career


@router.get("/career", response_model=List[CareerResponse])
def get_all_careers_route(db: Collection = Depends(get_db)):
    return get_all_careers(db)


@router.put("/career/{career_id}", response_model=CareerResponse)
def update_career_route(career_id: str, career: CareerUpdate, db: Collection = Depends(get_db)):
    updated_career = update_career(db, career_id, career)
    if not updated_career:
        raise HTTPException(status_code=404, detail="Career Not Found!!!")
    return updated_career


@router.delete("/career/{career_id}", response_model=bool)
def delete_career_route(career_id: str, db: Collection = Depends(get_db)):
    success = delete_career(db, career_id)
    if not success:
        raise HTTPException(status_code=404, detail="Career Not Found!!!")
    return success
