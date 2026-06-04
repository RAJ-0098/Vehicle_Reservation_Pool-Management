from fastapi import APIRouter,Depends,HTTPException
from models import *
from db import get_db
from app.schemas.Tripdetails_sch import TripCheckin,TripCheckout
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tripdetails",tags=["TripDetails"])


###Create Trip
@router.post("/chekcout")

def trip_checkout(CT:TripCheckout,db:Session=Depends(get_db)):
    reservation=(db.query(Vehicle_Reservation)
          .filter(Vehicle_Reservation.id == CT.reservation_id)
          .first())
    if not reservation:
        raise HTTPException(status_code=400,detail="Cannot find any reservation")
    vehicle=(db.query(Vehicle)
             .filter(Vehicle.id == reservation.vehicle_id)
             .first())
    if not vehicle:
        raise HTTPException(status_code=400,detail="Vehicle not reserved")
    if vehicle.status != Vehicle_status.RESERVED:
        raise HTTPException(status_code=400,detail=" Vehicle should be reserved first")
    
    existing_trip=(db.query(Trip_details)
                   .filter(Trip_details.reservation_id==reservation.id,
                           Trip_details.checkedin_time==None)
                           .first()
                   )
    if existing_trip:
        raise HTTPException(status_code=400,detail="Trip already exists")
    
    new_trip = Trip_details(
    reservation_id=CT.reservation_id,
    start_odometer=vehicle.current_odometer,
    end_odometer=None,
    checkedin_time=None,
    start_fuel=CT.start_fuel,
    end_fuel=None,
    expected_return_date=CT.expected_return_date,
    actual_return_date=None
    )

    db.add(new_trip)
    db.flush()
    
    vehicle.status = Vehicle_status.IN_USE

    vehicle_log = Vehicle_log(
    vehicle_id=reservation.vehicle_id,
    employee_id=reservation.employee_id,
    department_id=reservation.department_id,
    timestamp=datetime.now(),
    action=Action.CHECKED_OUT
)
    db.add(vehicle_log)
    db.commit()
    db.refresh(new_trip)
    return new_trip


@router.get("/checkout")
def get_tripcheckout(db:Session=Depends(get_db)):
    return (db.query(Trip_details).all())



@router.put("/checkin")

def trip_checkin(CTI:TripCheckin,db:Session=Depends(get_db)):
    
    trip_update=(db.query(Trip_details)
          .filter(Trip_details.id == CTI.tripcheckout_id)
          .first())
    if not trip_update:
        raise HTTPException(status_code=400,detail="Trip not started yet")
    
    reservation=(db.query(Vehicle_Reservation)
          .filter(Vehicle_Reservation.id == trip_update.reservation_id)
          .first())
    if not reservation:
        raise HTTPException(status_code=400,detail="Cannot find any reservation")
    
    if trip_update.end_odometer is not None:
        raise HTTPException(status_code=400,detail="invalid odometer ")
    

    if trip_update.end_fuel is not None:
        raise HTTPException(status_code=400,detail="Invalid fuel")
    

    if trip_update.start_odometer is None:
        raise HTTPException(status_code=400,detail="Start odometer invalid")
    

    if CTI.end_fuel>trip_update.start_fuel:
        raise HTTPException(status_code=400,detail="invalid fuel suspicious")
    

    if CTI.end_odometer < trip_update.start_odometer:
        raise HTTPException(status_code=400,detail="Suspicious ,invalid odometer")
    


    vehicle=(db.query(Vehicle)
             .filter(Vehicle.id == reservation.vehicle_id)
             .first())
    
    if vehicle.status != Vehicle_status.IN_USE:
        raise HTTPException(status_code=400,detail="suspicious , vehicle is not matching")
    
    trip_update.end_odometer = CTI.end_odometer
    trip_update.end_fuel = CTI.end_fuel
    trip_update.checkedin_time = datetime.now()
    trip_update.actual_return_date=datetime.now()


    vehicle.current_odometer = CTI.end_odometer

    checkin_log = Vehicle_log(
        vehicle_id=reservation.vehicle_id,
        employee_id=reservation.employee_id,
        department_id=reservation.department_id,
        timestamp=datetime.now(),
        action=Action.CHECKED_IN
    )


    if vehicle.current_odometer >= vehicle.maintenance_kms:
        vehicle.status = Vehicle_status.MAINTENANCE
    

        maintenance = Maintenance_schedule(
            vehicle_id = vehicle.id,
            Maintenance_start = datetime.now(),
            Maintenance_end = None,
            description = "Auto Scheduled to maintenance"
    )
        db.add(maintenance)
        db.flush()

        maintenance_log = Vehicle_log(
                vehicle_id=reservation.vehicle_id,
                employee_id=reservation.employee_id,
                department_id=reservation.department_id,
                timestamp=datetime.now(),
                action=Action.MAINTENANCE_START
    )
        
        db.add(maintenance_log)
        db.flush()

    else:
        vehicle.status = Vehicle_status.AVAILABLE


    reservation.reservation_end = datetime.now()
    
    db.add(checkin_log)
    db.commit()
    db.refresh(trip_update)
    return trip_update



@router.put("/{id}")
def get_overdue_stat(trip_id:int,db:Session=Depends(get_db)):

    trip = (db.query(Trip_details)
            .filter(Trip_details.id == trip_id)
            .first())
    if not trip: 
        raise HTTPException(status_code=400,detail="Trip doesnot count")

    reservation=(db.query(Vehicle_Reservation)
                 .filter(Vehicle_Reservation.id==trip.reservation_id)
                 .first())
    if not reservation:
        raise HTTPException(status_code=400,detail="No matching reservation")
    vehicle = (db.query(Vehicle)
               .filter(Vehicle.id == reservation.vehicle_id)
               .first())
    if not vehicle:
        raise HTTPException(status_code=400,detail="Vehicle is not matching")
    
    if trip.expected_return_date < datetime.now():
        action = Action.OVERDUE

    vehicle_log = Vehicle_log(
    vehicle_id=reservation.vehicle_id,
    employee_id=reservation.employee_id,
    department_id=reservation.department_id,
    timestamp=datetime.now(),
    action=Action.OVERDUE
    )
    db.add(vehicle_log)
    db.commit()
    db.refresh(vehicle_log)

    return action




