from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from typing import List
from ...db.database import get_db
from ...models.schemas import PDIBase, PDIInDB
from ...services.repository import get_pdi, get_all_pdi, update_pdi, delete_pdi

router = APIRouter()


@router.post("/pdi", response_model=PDIInDB)
def create_pdi(pdi: PDIBase, db: Collection = Depends(get_db)) -> PDIInDB:
    pdi_dict = pdi.model_dump()  # Atualizado para usar model_dump
    pdi_dict['date_add'] = datetime.now(timezone.utc)
    try:
        result = db["pdi"].insert_one(pdi_dict)
        if result.inserted_id:
            return PDIInDB(**{**pdi_dict, "id": str(result.inserted_id)})
        else:
            raise HTTPException(status_code=500, detail="Failed to insert PDI")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/pdi/{pdi_id}", response_model=PDIInDB)
def get_pdi_route(pdi_id: str, db: Collection = Depends(get_db)):
    pdi = get_pdi(db, pdi_id)
    if not pdi:
        raise HTTPException(status_code=404, detail="PDI not found")
    return pdi


@router.get("/pdi", response_model=List[PDIInDB])
def get_all_pdi_route(db: Collection = Depends(get_db)):
    return get_all_pdi(db)


@router.put("/pdi/{pdi_id}", response_model=PDIInDB)
def update_pdi_route(pdi_id: str, pdi: PDIBase, db: Collection = Depends(get_db)):
    updated_pdi = update_pdi(db, pdi_id, pdi)
    if not updated_pdi:
        raise HTTPException(status_code=404, detail="PDI not found")
    return updated_pdi


@router.delete("/pdi/{pdi_id}", response_model=bool)
def delete_pdi_route(pdi_id: str, db: Collection = Depends(get_db)):
    success = delete_pdi(db, pdi_id)
    if not success:
        raise HTTPException(status_code=404, detail="PDI not found")
    return success
