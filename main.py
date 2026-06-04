from fastapi import FastAPI
from db import engine, Base
from app.routes import departments
from app.routes.departments import router as dept_router
from app.routes.employes import router as emp_router
from app.routes.vehicles import router as vehicle_router
from app.routes.vehiclereservation import router as reserve_router
from app.routes.tripdetails import router as trip_router
from app.routes.maintenance import router as maintenance_router
from models import*


app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(dept_router)
app.include_router(vehicle_router)
app.include_router(emp_router)
app.include_router(reserve_router)
app.include_router(trip_router)
app.include_router(maintenance_router)

@app.get("/")

def home():
    return{"API is running"}
