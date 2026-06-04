from fastapi import APIRouter,Depends,HTTPException
from db import get_db
from models import *
from sqlalchemy.orm import Session
from app.schemas.vehiclereservation_sch import CreateVehicleReservation,VehiclereservationResponse,VehiclereservationUpdate

router = APIRouter(prefix="/vehiclereservation",tags=["Vehicle Reservation"])


### CREATE VEHICLE RESESRVATION 

@router.post("/")

def vehicle_reservation(VR:CreateVehicleReservation,db:Session=Depends(get_db)):
    try:
        with db.begin():
            ###check for department
            department=(db.query(Department)
                        .filter(Department.id == VR.department_id)
                        .first())
            if not department:
                raise HTTPException(status_code=400,detail="Department doesnot exists")
            
            ### check for employee
            employee=(db.query(Employee)
                    .filter(Employee.id == VR.employee_id)
                    .first())
            if not employee:
                raise HTTPException(status_code=400,detail="employee doesnot exists")
            
            ###check for vehicle
            vehicle=(db.query(Vehicle)
                    .filter(Vehicle.id == VR.vehicle_id)
                    .with_for_update()
                    .first())
            if not vehicle : 
                raise HTTPException(status_code=400,detail="Vehicle doesnot exists")
            
            ### check for licence validation 
            ###Driving_license=(db.query(Employee).filter(Employee.DL_date < datetime.now()).first())
            
            if employee.DL_date < datetime.now():
                raise HTTPException(status_code=400,detail="License should be renewed for further reservation")


            ###check for vehicle_quota limit 

            active_reservations = (
            db.query(Vehicle_Reservation)
            .filter(
                Vehicle_Reservation.employee_id == employee.id,
                Vehicle_Reservation.reservation_end == None
            )
            .count()
        )
            ### check for employee belongs to department or not 

            if employee.department_id != department.id:
                raise HTTPException(status_code=400,detail="Employee does not belong to selected department")  
            
            if vehicle.department_id != department.id:
                raise HTTPException(status_code=400,detail="Vehicle doesnot belong to this department")
            
            if active_reservations >= employee.vehicle_quota:
                raise HTTPException(
                status_code=400,
                detail="Enni kavali raa neeku"
            )

            ###Check for Vehicle Status 

            if vehicle.status != Vehicle_status.AVAILABLE:
                raise HTTPException(status_code=400,detail="Vehicle not available")    

            new_vehicle_reservation = Vehicle_Reservation(
                vehicle_id = VR.vehicle_id,
                department_id= VR.department_id,
                employee_id= VR.employee_id
            )
            db.add(new_vehicle_reservation)
            db.flush()
            vehicle.status = Vehicle_status.RESERVED
            print("Before commit:", vehicle.status)
            vehicle_log=Vehicle_log(
                vehicle_id=vehicle.id,
                employee_id=new_vehicle_reservation.employee_id,
                department_id=new_vehicle_reservation.department_id,
                timestamp=datetime.now(),
                action=Action.RESERVED
            )

            db.add(vehicle_log) 
            print("After commit:", vehicle.status)
            db.refresh(new_vehicle_reservation)

            return new_vehicle_reservation

    except:
        raise HTTPException(status_code=500,detail="Reservation servicing  is not funtioning ")



@router.get("/logs")

def get_logs(db:Session=Depends(get_db)):
    return (db.query(Vehicle_log).all())

@router.get("/reservations")
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Vehicle_Reservation).all()
