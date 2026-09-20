
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.responses import JSONResponse

DATABASE_URL = "sqlite:///./employees.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Float, nullable=False)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API",
    description="RESTful API for managing employee records",
    version="1.0.0"
)


class EmployeeCreate(BaseModel):

    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    age: int = Field(..., ge=18, le=65)
    department: str = Field(..., min_length=2, max_length=50)
    salary: float = Field(..., gt=0)


class EmployeeResponse(BaseModel):

    id: int
    name: str
    email: str
    age: int
    department: str
    salary: float

    class Config:
        from_attributes = True


@app.get("/", tags=["Health"])
def home():

    return {
        "message": "Employee Management API is running",
        "status": "success",
        "documentation": "/docs"
    }


@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=201,
    tags=["Employees"]
)
def create_employee(employee: EmployeeCreate):

    db = SessionLocal()

    try:

        existing_employee = (
            db.query(Employee)
            .filter(Employee.email == employee.email)
            .first()
        )

        if existing_employee:

            raise HTTPException(
                status_code=400,
                detail="Employee with this email already exists"
            )

        new_employee = Employee(
            name=employee.name,
            email=employee.email,
            age=employee.age,
            department=employee.department,
            salary=employee.salary
        )

        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return new_employee

    finally:

        db.close()


@app.get(
    "/employees",
    response_model=list[EmployeeResponse],
    tags=["Employees"]
)
def get_employees():

    db = SessionLocal()

    try:

        return db.query(Employee).all()

    finally:

        db.close()


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    tags=["Employees"]
)
def get_employee(employee_id: int):

    db = SessionLocal()

    try:

        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if employee is None:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return employee

    finally:

        db.close()


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    tags=["Employees"]
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeCreate
):

    db = SessionLocal()

    try:

        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if employee is None:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        existing_email = (
            db.query(Employee)
            .filter(
                Employee.email == employee_data.email,
                Employee.id != employee_id
            )
            .first()
        )

        if existing_email:

            raise HTTPException(
                status_code=400,
                detail="Another employee already uses this email"
            )

        employee.name = employee_data.name
        employee.email = employee_data.email
        employee.age = employee_data.age
        employee.department = employee_data.department
        employee.salary = employee_data.salary

        db.commit()
        db.refresh(employee)

        return employee

    finally:

        db.close()


@app.delete(
    "/employees/{employee_id}",
    tags=["Employees"]
)
def delete_employee(employee_id: int):

    db = SessionLocal()

    try:

        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if employee is None:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        db.delete(employee)
        db.commit()

        return {
            "message": "Employee deleted successfully",
            "employee_id": employee_id
        }

    finally:

        db.close()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong on the server"
        }
    )
