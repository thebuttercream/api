from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..postgres.database import get_db
from ..model import schemas
from ..model.models import Employees
from ..services import repository
from ..tools.logging import logger

router = APIRouter()


@router.post("/admin", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating Employee With Email: {employee.email}!")
    db_employee = repository.get_user_by_email(db, email=employee.email)
    if db_employee:
        logger.warning(f"Employee With Email {employee.email} Already Exists!!!")
        raise HTTPException(status_code=400, detail="Email Already Registered!")
    created_employee = repository.create_user(db=db, user=employee)
    logger.info(f"Employee Created With ID: {created_employee.id}!")
    return created_employee


@router.get("/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching Employee With ID: {employee_id}!")
    try:
        employee_id_int = employee_id
    except (ValueError, IndexError):
        logger.warning(f"Invalid Employee ID Format: {employee_id}!!!")
        raise HTTPException(status_code=400, detail="Invalid Employee ID Format!!!")

    db_employee = repository.get_employee(db, employee_id=employee_id_int)
    if db_employee is None:
        logger.warning(f"Employee With ID {employee_id} Not Found!!!")
        raise HTTPException(status_code=404, detail="Employee Not Found!!!")
    return db_employee


@router.get("/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching employees With Skip: {skip}, Limit: {limit}!")
    employees = repository.get_employees(db, skip=skip, limit=limit)
    return employees


@router.post("/identify", response_model=schemas.Employee)
def identify_employee(cpf: schemas.CPFIdentify, db: Session = Depends(get_db)):
    logger.info(f"Identifying Employee With CPF: {cpf.cpf}!")
    db_employee = repository.get_employee_by_cpf(db, cpf=cpf.cpf)
    if db_employee is None:
        logger.warning(f"Employee With CPF {cpf.cpf} Not Found!!!")
        raise HTTPException(status_code=404, detail="Employee Not Found!!!")
    return db_employee


@router.post("/register", response_model=schemas.Employee)
def register_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering Employee With Email: {Employees.email}")
    db_employee = repository.get_user_by_email(db, email=Employees.email)
    if db_employee:
        logger.warning(f"Employee With Email {Employees.email} Already Exists!")
        raise HTTPException(status_code=400, detail="Email Already Registered!")
    created_employee = repository.create_user(db=db, user=employee)
    logger.info(f"employee Registered With ID: {created_employee.id}!")
    return created_employee


@router.post("/anonymous", response_model=schemas.Employee)
def create_anonymous_employee(db: Session = Depends(get_db)):
    logger.info("Creating Anonymous Employee!")
    anonymous_employee = repository.create_anonymous_employee(db)
    logger.info(f"Anonymous Employee Created With ID: {anonymous_employee.id}!")
    return anonymous_employee
