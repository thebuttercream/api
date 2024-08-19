import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from dotenv import load_dotenv
from jose import jwt
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..model import models, schemas
from ..tools.logging import logger
from . import security

load_dotenv()

logger = logging.getLogger("Application")


def create_token(db: Session, token: str, user_id: int):
    logger.info(f"Creating token for user ID: {user_id}")
    db_token = models.Token(token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    logger.debug(f"Token created: {db_token.token}")
    return db_token


def mark_token_as_used(db: Session, token: str):
    logger.info(f"Marking token as used: {token}")
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token:
        db_token.is_used = True
        db.commit()
        db.refresh(db_token)
        logger.debug(f"Token marked as used: {token}")
    else:
        logger.warning(f"Token not found: {token}")
    return db_token


def is_token_used(db: Session, token: str):
    logger.debug(f"Checking if token is used: {token}")
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token and db_token.is_used:
        logger.debug(f"Token is used: {token}")
        return True
    logger.debug(f"Token is not used: {token}")
    return False


def create_access_token(data: dict, expires_delta: timedelta):
    logger.debug("Creating access token")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, security.SECRET_KEY, algorithm=security.ALGORITHM)
    logger.info("Access token created")
    return encoded_jwt


def get_user_by_email(db: Session, email: str):
    logger.info(f"Fetching user with email: {email}")
    return db.query(models.Employees).filter(models.Employees.email == email).first()


def create_user(db: Session, user: schemas.EmployeeCreate):
    logger.debug(f"Creating user with email: {user.email}")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Employees(name=user.name, email=user.email, cpf=user.cpf, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}")
    return db_user


def create_anonymous_employee(db: Session):
    logger.debug("Creating anonymous employee")
    anonymous_employee = models.Employees(
        name="Anonymous",
        email=None,
        cpf=None,
        hashed_password=None
    )
    db.add(anonymous_employee)
    db.commit()
    db.refresh(anonymous_employee)
    logger.info(f"Anonymous employee created with ID: {anonymous_employee.id}")
    return anonymous_employee


def get_employee_by_cpf(db: Session, cpf: str):
    logger.debug(f"Fetching employee with CPF: {cpf}")
    return db.query(models.Employees).filter(models.Employees.cpf == cpf).first()


def create_admin_user(db: Session):
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        admin_cpf = os.getenv("ADMIN_CPF")
        admin_name = os.getenv("ADMIN_NAME")

        if not all([admin_email, admin_password, admin_cpf, admin_name]):
            logger.error("Admin user details are not set in environment variables.")
            return

        logger.debug(f"Admin email: {admin_email}, Admin name: {admin_name}")

        user = db.query(models.Employees).filter(models.Employees.email == admin_email).first()
        if not user:
            hashed_password = security.get_password_hash(admin_password)
            admin_user = models.Employees(
                name=admin_name,
                email=admin_email,
                cpf=admin_cpf,
                hashed_password=hashed_password
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.debug(f"Admin user created with email: {admin_email}")
        else:
            logger.debug(f"Admin user already exists with email: {admin_email}")
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")


def get_employee_count(db: Session):
    logger.info("Fetching total count of employees")
    return db.query(models.Employees).count()


def get_employee(db: Session, employee_id: int):
    logger.debug(f"Fetching employee with ID: {employee_id}")
    try:
        return db.query(models.Employees).filter(models.Employees.id == employee_id).first()
    except Exception as e:
        logger.error(f"Error fetching employee: {e}")
        return None


def get_employees(db: Session, skip: int = 0, limit: int = 10):
    logger.debug(f"Fetching employees with skip: {skip}, limit: {limit}")
    return db.query(models.Employees).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    logger.debug(f"Creating employee with email: {employee.email}")
    db_employee = models.Employees(name=employee.name, email=employee.email, cpf=employee.cpf)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    logger.info(f"Employee created with ID: {db_employee.id}")
    return db_employee
