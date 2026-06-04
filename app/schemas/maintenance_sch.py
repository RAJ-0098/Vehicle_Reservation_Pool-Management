from pydantic import BaseModel
from models import*

class CreateMaintenance(BaseModel):
      vehicle_id:int
      Maintenance_start:datetime
      Maintenance_end:datetime
      description:str


class Config:
    from_attributes:True


class MaintenanceResponse(BaseModel):
      id:int


class Config:
    from_attributes:True

class MaintenanceUpdate(BaseModel):
      id:int


class Config:
    from_attributes:True




