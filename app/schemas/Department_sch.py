from pydantic import BaseModel
from models import*


class CreateDepartment(BaseModel):
    title:str

class Config:
    from_attributes:True



class DepartmentResponse(BaseModel):
    id:int
class Config:
    from_attributes:True


class DepartmentUpdate(BaseModel):
    id:int
class Config:
    from_attributes:True