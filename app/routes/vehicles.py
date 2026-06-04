from fastapi import APIRouter,Depends,HTTPException
from models import *
from db import get_db
from sqlalchemy.orm import Session
from app.schemas.Vehicle_sch import CreateVehicle,VehicleUpdate
router = APIRouter(prefix="/vehicles",tags=["Vehicle"])



###VEHICLE CREATION 

@router.post("/")
def create_vehicle(vd:CreateVehicle,db:Session = Depends(get_db)):
    existing_vehicle=(db.query(Vehicle)
                      .filter(Vehicle.vehicle_number== vd.vehicle_number)
                      .first())
    if existing_vehicle:
        raise HTTPException(status_code=400,detail="Vehicle already exists")
    
    new_vehicle=Vehicle(
        department_id=vd.department_id,
        vehicle_type=vd.vehicle_type,
        vehicle_number=vd.vehicle_number,
        maintenance_interval=vd.maintenance_interval,
        maintenance_kms=vd.maintenance_kms,
        status = Vehicle_status.AVAILABLE
    )

    db.add(new_vehicle)
    db.flush()
    
    vehicle_log=Vehicle_log(
        vehicle_id=new_vehicle.id,
        employee_id=None,
        department_id=new_vehicle.department_id,
        timestamp=datetime.now(),
        action=Action.CREATED
    )

    db.add(vehicle_log) 
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle


###VEHICLE LOGS 

@router.get("/logs")
def get_logs(db:Session=Depends(get_db)):
    return (db.query(Vehicle_log).all())


### GET ALL VEHICLES

@router.get("/")
def get_vehicle(db:Session=Depends(get_db)):
    return (db.query(Vehicle).all())


### GET VEHCILE BY ID 


@router.get("/{id}")
def get_vehicle(id:int, db:Session=Depends(get_db)):
    vehicle=(db.query(Vehicle)
             .filter(Vehicle.id == id)
             .first())
    return vehicle


###VEHICLE CURRENT STATUS

@router.get("/{id}/status")
def get_status(id:int,db:Session=Depends(get_db)):
    existing_vehicle=(db.query(Vehicle)
             .filter(Vehicle.id==id)
             .first())
    if  not existing_vehicle:
        raise HTTPException(status_code=400,detail="Vehicle doesnot exists")
    return {
        "vehicle_id" : existing_vehicle.id,
        "vehicle_number": existing_vehicle.vehicle_number,
        "status":existing_vehicle.status
    }