from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from db import get_db
from app.schemas.maintenance_sch import CreateMaintenance,MaintenanceResponse,MaintenanceUpdate
from models import *


router = APIRouter(prefix="/maintenance",tags=["Maintenance"])





@router.get("/")
def get_maintenance(db:Session=Depends(get_db)):
    return db.query(Maintenance_schedule).all()



@router.put("/")
def complete_maintenance(MID:int,db:Session=Depends(get_db)):
    maintenance = (db.query(Maintenance_schedule)
                   .filter(Maintenance_schedule.id == MID)
                   .first())
    
    if not maintenance:
        raise HTTPException(status_code=400,detail="No maintenance scheduled")
    
    if maintenance.Maintenance_end != None:
        raise HTTPException(status_code=400,detail="Maintenance completed")
    
    vehicle = (db.query(Vehicle)
               .filter(Vehicle.id == maintenance.vehicle_id)
               .first())
    if not vehicle :
        raise HTTPException(status_code=400,detail="Suspicious maintenance vehicle mismatched")
    
    maintenance.Maintenance_end = datetime.now()

    vehicle.status = Vehicle_status.AVAILABLE
    
    vehicle.maintenance_kms  +=vehicle.maintenance_interval

    vehicle_log = Vehicle_log(
                vehicle_id=vehicle.id,
                employee_id=None,
                department_id=vehicle.department_id,
                timestamp=datetime.now(),
                action=Action.MAINTENANCE_END
    )
    db.add(vehicle_log)
    db.commit()

    return {
    "message": "Maintenance completed successfully",
    "vehicle_id": vehicle.id,
    "vehicle_status": vehicle.status,
    "maintenance_kms": vehicle.maintenance_kms
}








