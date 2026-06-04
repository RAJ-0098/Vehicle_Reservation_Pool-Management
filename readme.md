

# Enterprise Vehicle Pool Management System 🚗

## Overview




                            Corporate Vehicle Pool Management 
Business Context & Value Proposition:

The system manages a company's shared fleet of vehicles, including cars, bikes, and vans, used by employees for official business activities such as client visits, inter-office travel, and field operations. The platform ensures efficient vehicle allocation, prevents double bookings, tracks vehicle usage, and maintains maintenance schedules. Proper control is essential to maximize fleet utilization while ensuring safety, compliance, and operational efficiency.


Business Capabilities & Rules:

###Department-Based Vehicle Access: Every vehicle belongs to a specific department or is shared across departments. Employees can reserve only vehicles they are authorized to access through their department.

###Reservation Scheduling: Employees can reserve vehicles for a specific time period. The system must prevent overlapping reservations for the same vehicle.

###Driver Eligibility Validation: Employees must possess a valid company-approved driving license. Reservations must be rejected if the license has expired.

###Reservation Quota Enforcement: Each employee has a configurable reservation limit. The system must prevent employees from exceeding their active reservation quota.

###Availability Enforcement: Vehicles can be reserved only when their status is AVAILABLE. Vehicles marked as RESERVED, IN_USE, MAINTENANCE, or OUT_OF_SERVICE cannot be booked.

###Maintenance Blocking: Vehicles scheduled for maintenance must be automatically excluded from reservation availability during the maintenance window.

###Check-Out Workflow: Before using a vehicle, employees must perform a check-out operation. Vehicle status changes from RESERVED to IN_USE.

###Check-In Workflow: Upon trip completion, employees must check the vehicle back in. The system records trip completion details and restores vehicle availability.

###Trip Tracking Validation: Every completed trip must record starting and ending odometer readings along with fuel levels before and after the trip. Invalid mileage or fuel data must be rejected.

###Audit Trail Generation: Every vehicle-related action must be logged, including reservations, check-outs, check-ins, cancellations, and maintenance activities. Logs must retain employee, vehicle, department, timestamp, and action details.

Ambiguity Areas for Developers to Resolve:

###Concurrent Reservation Handling: How should the system safely process simultaneous reservation requests for the same vehicle and overlapping time period without causing double bookings or inconsistent reservation records? 

###Vehicle Status Management: Should vehicle status be stored directly in the database and updated on every operation, or should it be dynamically derived from active reservations and maintenance schedules?

###Automatic Trip Expiry: How should the system handle vehicles that remain checked out beyond their expected return time and were never formally checked back in?

###Maintenance Conflict Validation: How should future maintenance schedules be validated against existing reservations to prevent scheduling conflicts?

###Transactional Consistency: How can reservation creation, vehicle status updates, trip tracking updates, and audit log creation be executed atomically so that partial failures do not leave inconsistent system data?




---

# Features

## Department Management

* Create and manage departments
* Associate employees and vehicles with departments

---

## Employee Management

* Employee registration
* Driving license validation
* Vehicle reservation quota management

---

## Vehicle Management

* Vehicle registration
* Vehicle status tracking
* Vehicle allocation to departments
* Odometer tracking
* Maintenance scheduling support

---

# Vehicle Status Lifecycle

The vehicle follows a controlled lifecycle:

```text
AVAILABLE
    ↓
RESERVED
    ↓
IN_USE
    ↓
AVAILABLE
    ↓
MAINTENANCE
    ↓
AVAILABLE
```

---

# Reservation System

## Reservation Features

* Reserve available vehicles
* Prevent reservation of unavailable vehicles
* Prevent reservation of vehicles under maintenance
* Enforce employee reservation quota
* Validate employee and department ownership

---

## Reservation Quota Enforcement

Each employee has a configurable reservation limit.

Example:

```text
Employee A → 1 active reservation
Manager → 3 active reservations
```

The system blocks new reservations if the employee exceeds the active reservation quota.

---

# Trip Management

## Checkout Process

During vehicle checkout:

* Reservation validation is performed
* Vehicle status changes from `RESERVED` → `IN_USE`
* Trip details are created
* Checkout logs are stored
* Start odometer is automatically taken from vehicle current odometer

---

## Checkin Process

During vehicle checkin:

* End odometer validation
* Fuel validation
* Distance calculation
* Vehicle odometer update
* Overdue validation
* Automatic maintenance detection
* Vehicle log creation
* Reservation completion

---

# Odometer-Based Maintenance System

The project uses a realistic mileage-based maintenance system.

---

## Vehicle Maintenance Fields

Each vehicle stores:

```text
current_odometer
maintenance_interval
maintenance_kms
```

---

## Maintenance Workflow

### Example

```text
Vehicle Created

Current Odometer = 0
maintenance Interval = 10000 km
Next maintenance = 10000 km
```

---

### After Trips

```text
Trip 1 → 300 km
Trip 2 → 500 km
Trip 3 → 700 km
```

Vehicle odometer increases continuously.

---

### Automatic Maintenance Trigger

During checkin:

```text
if current_odometer >= maintenance_kms
```

Then:

```text
Vehicle Status → MAINTENANCE
```

A maintenance schedule is automatically created.

---

## Maintenance Completion

When maintenance is completed:

* Vehicle becomes AVAILABLE again
* Next service target is updated

Example:

```text
Previous maintenance Target = 10000 km
maintenance Interval = 10000 km

New maintenance Target = 20000 km
```

---

# Overdue Trip Handling

The system detects overdue trips during checkin.

If:

```text
actual_return_time > expected_return_time
```

Then:

```text
OVERDUE log is generated
```

The vehicle is not permanently marked overdue.

---

# Vehicle Logs

The system maintains a complete activity history.

## Supported Actions

```text
CREATED
RESERVED
CHECKED_OUT
CHECKED_IN
OVERDUE
MAINTENANCE_START
MAINTENANCE_END
```

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic

---

# Database Concepts Used

* One-to-Many Relationships
* Foreign Keys
* Constraints
* Enumerations
* Transactions
* Database Migrations

---

# API Modules

## Department APIs

* Create Department
* Get Departments

## Employee APIs

* Create Employee
* Get Employees

## Vehicle APIs

* Create Vehicle
* Get Vehicles

## Reservation APIs

* Create Reservation
* Get Reservations

## Trip APIs

* Checkout Vehicle
* Checkin Vehicle
* Get Trip Details

## Maintenance APIs

* Complete Maintenance
* Get Maintenance Records

## Logs APIs

* Get Vehicle Logs

---

# Key Validations Implemented

## Reservation Validations

* Department existence validation
* Employee existence validation
* Vehicle existence validation
* License validation
* Vehicle availability validation
* Maintenance validation
* Reservation quota validation

---

## Trip Validations

* Duplicate trip prevention
* Vehicle state validation
* Odometer tampering prevention
* Fuel validation
* Overdue validation

---

# Real-World Concepts Implemented

* Enterprise fleet management
* Vehicle reservation systems
* Mileage-based maintenance scheduling
* Vehicle lifecycle tracking
* Activity auditing
* Automated operational constraints

---

# Future Improvements

* GPS integration
* Authentication & authorization
* Role-based access control
* Notification system
* Dashboard analytics
* IoT odometer integration
* Vehicle service cost tracking
* Fuel analytics
* Real-time vehicle monitoring

---

# Author

Raj Gopal Vadduri

