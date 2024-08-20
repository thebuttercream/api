from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional
from ..models.schemas import EmployeeCreate, EmployeeInDB, EmployeeUpdate
from . import security


def create_employee(db: Collection, employee: EmployeeCreate) -> EmployeeInDB:
    employee_dict = employee.model_dump()  # Atualizado para usar model_dump
    employee_dict['hashed_password'] = security.hash_password(employee.password)
    result = db["employees"].insert_one(employee_dict)
    return EmployeeInDB(**{**employee_dict, "id": str(result.inserted_id)})


def get_employee(db: Collection, employee_id: str) -> Optional[EmployeeInDB]:
    employee_data = db["employees"].find_one({"_id": ObjectId(employee_id)})
    if employee_data:
        return EmployeeInDB(**{**employee_data, "id": str(employee_data["_id"])})
    return None


def get_all_employees(db: Collection) -> list[EmployeeInDB]:
    employees = list(db["employees"].find())
    return [EmployeeInDB(**{**employee, "id": str(employee["_id"])}) for employee in employees]


def update_employee(db: Collection, employee_id: str, employee: EmployeeUpdate) -> Optional[EmployeeInDB]:
    update_data = employee.model_dump(exclude_unset=True)  # Atualizado para usar model_dump
    if "password" in update_data:
        update_data['hashed_password'] = security.hash_password(update_data.pop('password'))
    result = db["employees"].update_one({"_id": ObjectId(employee_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return get_employee(db, employee_id)


def delete_employee(db: Collection, employee_id: str) -> bool:
    result = db["employees"].delete_one({"_id": ObjectId(employee_id)})
    return result.deleted_count > 0
