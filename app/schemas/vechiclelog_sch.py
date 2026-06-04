from pydantic import BaseModel
from models import*

class Createvehiclelog(BaseModel):
    vehicle_id:int
    employee_id:int
    department_id:int


class Config:
    from_attributes:True

class VehiclelogResponse(BaseModel):
    id:int

class Config:
    from_attributes:True

    
    
    
