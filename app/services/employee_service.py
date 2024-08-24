from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional, List
from ..models.schemas import EmployeeUpdate, EmployeeBase, EmployeeResponse


def create_employee(db: Collection, employee: EmployeeBase) -> EmployeeResponse:
    employee_dict = employee.model_dump()
    result = db["employees"].insert_one(employee_dict)
    return EmployeeResponse(**{**employee_dict, "id": str(result.inserted_id)})


def get_employee(db: Collection, employee_id: str) -> Optional[EmployeeResponse]:
    employee_data = db["employees"].find_one({"_id": ObjectId(employee_id)})
    if employee_data:
        return EmployeeResponse(**{**employee_data, "id": str(employee_data["_id"])})
    return None


def get_all_employees(db: Collection) -> List[EmployeeResponse]:
    employees = list(db["employees"].find())
    return [EmployeeResponse(**{**employee, "id": str(employee["_id"])}) for employee in employees]


def update_employee(db: Collection, employee_id: str, employee: EmployeeUpdate) -> Optional[EmployeeResponse]:
    update_data = employee.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data.pop('password')
    result = db["employees"].update_one({"_id": ObjectId(employee_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return get_employee(db, employee_id)

def delete_employee(db: Collection, employee_id: str) -> bool:
    result = db["employees"].delete_one({"_id": ObjectId(employee_id)})
    return result.deleted_count > 0
