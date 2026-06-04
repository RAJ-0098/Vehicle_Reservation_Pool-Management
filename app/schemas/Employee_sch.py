from pydantic import BaseModel
from models import*


class CreateEmployee(BaseModel):
    name:str
    aadhar_card:int
    department_id:int
    DL_date:datetime
    vehicle_quota:int

class Config:
    from_attributes:True


class EmployeeResponse(BaseModel):
    id:int

class Config:
    from_attributes:True


class EmployeeUpdate(BaseModel):
    name :str
    aadhar_card:int
    department_id:int
    DL_date:datetime
    vehicle_quota:int

class Config:
    from_attributes:True
    