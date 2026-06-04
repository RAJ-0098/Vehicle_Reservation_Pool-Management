from models import *
from pydantic import BaseModel

class TripCheckout(BaseModel):
    reservation_id:int
    start_fuel:int
    expected_return_date:datetime


class Config:
    from_attributes:True


class TripCheckin(BaseModel):
    tripcheckout_id:int
    end_odometer:int
    end_fuel:int

class Config:
    from_attributes:True