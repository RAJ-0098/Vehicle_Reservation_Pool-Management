from pydantic import BaseModel
from models import*

class CreateVehicle(BaseModel):
    department_id:int
    vehicle_number:str
    vehicle_type:str
    maintenance_interval:int
    maintenance_kms:int


class VehicleResponse(BaseModel):
    id:int


class Config:
    from_attributes:True

class VehicleUpdate(BaseModel):
    department_id:int
    vehicle_number:str
    vehicle_type:str


class Config:
    from_attributes:True

class statusResponse(BaseModel):
    status:Enum


class Config:
    from_attributes:True