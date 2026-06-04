from pydantic import BaseModel
from models import*

class CreateVehicleReservation(BaseModel):
     employee_id:int
     department_id:int
     vehicle_id:int

class Config:
    from_attributes:True



class VehiclereservationResponse(BaseModel):
     id:int


class Config:
    from_attributes:True

class VehiclereservationUpdate(BaseModel):
     id:int


class Config:
    from_attributes:True
    












