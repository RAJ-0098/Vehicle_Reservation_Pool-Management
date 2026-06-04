from models import Department
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from db import get_db
from app.schemas.Department_sch import CreateDepartment,DepartmentResponse,DepartmentUpdate

router=APIRouter(prefix="/departments",tags=["Departments"])



###CREATE DEPARTMENT

@router.post("/")
def create_department(department:CreateDepartment,db:Session=Depends(get_db)):

    existing_department=(db.query(Department)
                         .filter(Department.title==department.title)
                         .first())
    if existing_department:
        raise HTTPException(status_code=400,detail="Department already exists")
    new_department=Department(
        title = department.title
    )
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


### GET ALL DEPARTMENTS

@router.get("/")
def get_departments(db:Session=Depends(get_db)):
    return (db.query(Department).all())


### GET DEPARTMENT BY ID 


@router.get("/{id}")
def get_deparments(id:int,db:Session=Depends(get_db)):
    department=(db.query(Department)
                .filter(Department.id == id)
                .first())
    if not department:
        raise HTTPException(status_code=400,detail="Department not exists")
    return department


@router.put("/")
def update_dept(id:int,updatedept:DepartmentUpdate,db:Session=Depends(get_db)):
    department = (db.query(Department)
                  .filter(Department.id == id)
                  .first())
    if not department:
        raise HTTPException(status_code=404,detail="depratment not found ")
    department.title = updatedept.title

    return department


    