from fastapi import Depends, HTTPException

from scheduling.calendar import NotEnoughDaysError
from scheduling.constants import TWO_YEAR_LEN_DAYS
from scheduling.patients import Patient, InvalidFractionTime
from scheduling.scheduler import Scheduler, ExtendScheduleError
from scheduling.utils import get_machine_pool, get_machine_calendar
from server.models import (
    MakeAppointmentRequest,
    MakeAppointmentResponse,
    GetLoadResponse,
)

from fastapi import FastAPI

app = FastAPI()


@app.post("/schedule", response_model=MakeAppointmentResponse)
def get_availability(
    request: MakeAppointmentRequest,
    machine_pool=Depends(get_machine_pool),
):
    try:
        patient = Patient.from_model(request)
    except InvalidFractionTime as e:
        raise HTTPException(422, detail=str(e))

    machine_calendar = get_machine_calendar(machine_pool, TWO_YEAR_LEN_DAYS)
    scheduler = Scheduler(
        period_length_days=365,
        machine_pool=machine_pool,
        patient_generator=None,
        machine_calendar=machine_calendar,
    )
    try:
        machine, shift = scheduler.process_patient(patient)
        return {"machine_name": machine.name(), "shift": shift}

    except ExtendScheduleError:
        raise HTTPException(status_code=404, detail="Can't schedule appointment")


@app.get("/load", response_model=GetLoadResponse)
def get_load(shift: int, machine_pool=Depends(get_machine_pool)):
    machine_calendar = get_machine_calendar(machine_pool, TWO_YEAR_LEN_DAYS)
    try:
        return machine_calendar.get_daily_load(shift)
    except NotEnoughDaysError:
        raise HTTPException(status_code=422, detail="Invalid skew")
