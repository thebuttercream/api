from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional
from ..models.schemas import PDIBase, PDIInDB


def create_pdi(db: Collection, pdi: PDIBase) -> PDIInDB:
    pdi_dict = pdi.model_dump()
    pdi_dict['date_add'] = datetime.now(timezone.utc)
    result = db["pdi"].insert_one(pdi_dict)
    return PDIInDB(**{**pdi_dict, "id": str(result.inserted_id)})


def get_pdi(db: Collection, pdi_id: str) -> Optional[PDIInDB]:
    pdi_data = db["pdi"].find_one({"_id": ObjectId(pdi_id)})
    if pdi_data:
        return PDIInDB(**{**pdi_data, "id": str(pdi_data["_id"])})
    return None


def get_all_pdi(db: Collection) -> list[PDIInDB]:
    pdi = list(db["pdi"].find())
    return [PDIInDB(**{**pdi, "id": str(pdi["_id"])}) for pdi in pdi]


def update_pdi(db: Collection, pdi_id: str, pdi: PDIBase) -> Optional[PDIInDB]:
    update_data = pdi.model_dump(exclude_unset=True)
    result = db["pdi"].update_one({"_id": ObjectId(pdi_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return get_pdi(db, pdi_id)


def delete_pdi(db: Collection, pdi_id: str) -> bool:
    result = db["pdi"].delete_one({"_id": ObjectId(pdi_id)})
    return result.deleted_count > 0
