from fastapi import APIRouter,Depends,HTTPException
from db import get_db
from models import*
from app.schemas.Employee_sch import CreateEmployee,EmployeeUpdate,EmployeeResponse
from sqlalchemy.orm import Session


router=APIRouter(prefix="/employee",tags=["Employee"])



### CREATE EMPLOYEE


@router.post("/")
def create_employee(employee:CreateEmployee,db:Session=Depends(get_db)):
    
    department = (db.query(Department)
                  .filter(Department.id ==employee.department_id)
                  .first())
    if not department:
        raise HTTPException (status_code=404,detail="Department not exists")
    
    
    existing_employee = (db.query(Employee)
                         .filter(Employee.aadhar_card==employee.aadhar_card)
                         .first())
    if existing_employee:
        raise HTTPException(status_code=400,detail="aadhar already exists")
    
    
    new_employee=Employee(
        name=employee.name,
        aadhar_card=employee.aadhar_card,
        department_id=employee.department_id,
        DL_date=employee.DL_date,
        vehicle_quota=employee.vehicle_quota
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


### GET EMPLOYEE BY ID 

@router.get("/{id}")

def get_employee(id:int,db:Session=Depends(get_db)):
    employee=(db.query(Employee)
              .filter(Employee.id == id)
              .first())
    if not employee:
        raise HTTPException(status_code=400,detail="Employee not found")
    return employee


### GET EMPLOYEE

@router.get("/")
def get_employee(db:Session=Depends(get_db)):
    return (db.query(Employee).all())


### EMPLOYEE UPDATE 

   
@router.put("/{id}")
def update_employee(id:int,updateemployee:EmployeeUpdate,db:Session=Depends(get_db)):
    employee=(db.query(Employee)
              .filter(Employee.id == id)
              .first())
    if not employee:
        raise HTTPException(status_code=400,detail="Employee not exists")
    
    employee.name=updateemployee.name
    employee.aadhar_card=updateemployee.aadhar_card
    employee.department_id=updateemployee.department_id
    employee.DL_date=updateemployee.DL_date
    employee.vehicle_quota=updateemployee.vehicle_quota

    db.commit()
    db.refresh(employee)
    return employee