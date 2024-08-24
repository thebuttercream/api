from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from typing import List
from ...db.database import get_db
from ...models.schemas import EmployeeCreate, EmployeeInDB, EmployeeUpdate
from ...services.employee_service import (
    create_employee,
    get_employee,
    get_all_employees,
    update_employee,
    delete_employee,
)

router = APIRouter()


@router.post("/employee", response_model=EmployeeInDB)
def create_employee_route(employee: EmployeeCreate, db: Collection = Depends(get_db)):
    return create_employee(db, employee)


@router.get("/employee/{employee_id}", response_model=EmployeeInDB)
def get_employee_route(employee_id: str, db: Collection = Depends(get_db)):
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee Not Found!!!")
    return employee


@router.get("/employee", response_model=List[EmployeeInDB])
def get_all_employees_route(db: Collection = Depends(get_db)):
    return get_all_employees(db)


@router.put("/employee/{employee_id}", response_model=EmployeeInDB)
def update_employee_route(employee_id: str, employee: EmployeeUpdate, db: Collection = Depends(get_db)):
    updated_employee = update_employee(db, employee_id, employee)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee Not Found!!!")
    return updated_employee


@router.delete("/employee/{employee_id}", response_model=bool)
def delete_employee_route(employee_id: str, db: Collection = Depends(get_db)):
    success = delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee Not Found!!!")
    return success
