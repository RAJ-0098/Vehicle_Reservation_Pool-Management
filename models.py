from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Enum as SQLEnum,Text
from datetime import datetime
from enum import Enum
from db import Base



class Department(Base):
    __tablename__="departments"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)



class Employee(Base):
    __tablename__="employees"
    id=Column(Integer,primary_key=True)
    aadhar_card=Column(Integer,unique=True,nullable=False)
    name=Column(String,nullable=False)
    department_id=Column(Integer,ForeignKey("departments.id"))
    DL_date=Column(DateTime,nullable=False)
    vehicle_quota=Column(Integer,nullable=True)


class Vehicle_status(str,Enum):
    AVAILABLE="AVAILABLE"
    RESERVED="RESERVED"
    IN_USE="IN_USE"
    MAINTENANCE="MAINTENANCE"
    OVERDUE="OVERDUE"
    OUT_OF_SERVICE="OUT_OF_SERVICE"


class Vehicle(Base):
    __tablename__="vehicles"
    id=Column(Integer,primary_key=True)
    vehicle_number=Column(String,unique=True,nullable=False)
    status=Column(SQLEnum(Vehicle_status),default=Vehicle_status.AVAILABLE,nullable=False)
    department_id=Column(Integer,ForeignKey("departments.id"))
    vehicle_type=Column(String,nullable=False)
    current_odometer=Column(Integer,default=0)
    maintenance_interval = Column(Integer,nullable=False)
    maintenance_kms = Column(Integer,nullable=False)



class Vehicle_Reservation(Base):
    __tablename__="vehiclereservations"
    id=Column(Integer,primary_key=True)
    employee_id=Column(Integer,ForeignKey("employees.id"))
    department_id=Column(Integer,ForeignKey("departments.id"))
    vehicle_id=Column(Integer,ForeignKey("vehicles.id"))
    reservation_start=Column(DateTime,nullable=False,default=datetime.now())
    reservation_end=Column(DateTime,nullable=True)




class Maintenance_schedule(Base):
    __tablename__="maintenanceschedule"
    id=Column(Integer,primary_key=True)
    vehicle_id=Column(Integer,ForeignKey("vehicles.id"))
    Maintenance_start=Column(DateTime,nullable=False)
    Maintenance_end=Column(DateTime,nullable=True)
    description=Column(Text,nullable=True)
    


class Action(str,Enum):
    CREATED="CREATED"
    RESERVED="RESERVED"
    OVERDUE="OVERDUE"
    OUT_OF_SERVICE="OUT_OF_SERVICE"
    CHECKED_OUT="CHECKED_OUT"
    CHECKED_IN="CHECKED_IN"
    CANCELLATION="CANCELLATION"
    MAINTENANCE_START="MAINTENANCE_START"
    MAINTENANCE_END="MAINTENANCE_END"



class Vehicle_log(Base):
    __tablename__="vehiclelogs"
    id=Column(Integer,primary_key=True)
    vehicle_id=Column(Integer,ForeignKey("vehicles.id"))
    employee_id=Column(Integer,ForeignKey("employees.id"),nullable=True)
    department_id=Column(Integer,ForeignKey("departments.id"))
    timestamp=Column(DateTime)
    action=Column(SQLEnum(Action),nullable=False)

class Trip_details(Base):
    __tablename__="tripdetails"
    id=Column(Integer,primary_key=True)
    reservation_id=Column(Integer,ForeignKey("vehiclereservations.id"))
    start_odometer=Column(Integer,nullable=False,default="0")
    end_odometer=Column(Integer,nullable=True)
    start_fuel=Column(Integer,nullable=False)
    end_fuel=Column(Integer,nullable=True)
    checkedout_time=Column(DateTime,default=datetime.now(),nullable=False)
    checkedin_time=Column(DateTime,nullable=True)
    trip_start_date=Column(DateTime,default=datetime.now(),nullable=False)
    expected_return_date=Column(DateTime,nullable=False)
    actual_return_date=Column(DateTime,nullable=True)






