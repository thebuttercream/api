import logging

from sqlalchemy.orm import Session

from app.model.models import Employees

logger = logging.getLogger("Application")


def initialize_db(db: Session):
    employees = [
        {"firstname": "Ana", "lastname": "Silva", "email": "ana.silva@example.com", "cpf": "12345678901",
         "is_manager": True, "hashed_password": "hashed_password_ana"},
        {"firstname": "Carlos", "lastname": "Oliveira", "email": "carlos.oliveira@example.com", "cpf": "10987654321",
         "is_manager": False, "hashed_password": "hashed_password_carlos"},
        {"firstname": "Maria", "lastname": "Santos", "email": "maria.santos@example.com", "cpf": "11223344556",
         "is_manager": False, "hashed_password": "hashed_password_maria"},
        {"firstname": "Pedro", "lastname": "Costa", "email": "pedro.costa@example.com", "cpf": "22334455667",
         "is_manager": False, "hashed_password": "hashed_password_pedro"},
        {"firstname": "Laura", "lastname": "Martins", "email": "laura.martins@example.com", "cpf": "33445566778",
         "is_manager": True, "hashed_password": "hashed_password_laura"},
        {"firstname": "Lucas", "lastname": "Pereira", "email": "lucas.pereira@example.com", "cpf": "44556677889",
         "is_manager": False, "hashed_password": "hashed_password_lucas"},
        {"firstname": "Juliana", "lastname": "Almeida", "email": "juliana.almeida@example.com", "cpf": "55667788990",
         "is_manager": False, "hashed_password": "hashed_password_juliana"},
        {"firstname": "Ricardo", "lastname": "Fernandes", "email": "ricardo.fernandes@example.com",
         "cpf": "66778899001", "is_manager": True, "hashed_password": "hashed_password_ricardo"},
        {"firstname": "Fernanda", "lastname": "Melo", "email": "fernanda.melo@example.com", "cpf": "77889900112",
         "is_manager": False, "hashed_password": "hashed_password_fernanda"},
        {"firstname": "Gabriel", "lastname": "Gomes", "email": "gabriel.gomes@example.com", "cpf": "88990011223",
         "is_manager": False, "hashed_password": "hashed_password_gabriel"},
    ]

    existing_emails = {employee.email for employee in db.query(Employees.email).all()}

    for employee in employees:
        if employee['email'] in existing_emails:
            logger.debug(f"Employee already exists in the database: {employee['email']}")
        else:
            db_employee = Employees(**employee)
            db.add(db_employee)
            logger.debug(f"Employee added: {db_employee.firstname} {db_employee.lastname}")

    db.commit()
    logger.debug("Employees database initialization completed.")
