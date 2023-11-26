from typing import List

from fastapi import Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware

from scheduling.calendar import NotEnoughDaysError
from scheduling.constants import TWO_YEAR_LEN_DAYS
from scheduling.diseases import CANCER_MAP
from scheduling.machine_pool import MachinePool
from scheduling.patients import Patient, InvalidFractionTime, PatientGen
from scheduling.scheduler import Scheduler, ExtendScheduleError
from scheduling.utils import (
    get_machine_pool,
    get_machine_calendar,
    get_patient_generator,
)
from server.models import (
    MakeAppointmentRequest,
    MakeAppointmentResponse,
    GetLoadResponse,
    PatientModel,
    CancerModel,
    PagedResponse,
)

from fastapi import FastAPI

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "localhost", "http://127.0.0.1", "http://0.0.0.0"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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


@app.get("/patients", response_model=PagedResponse[PatientModel])
def get_patient(
    limit: int = 100, patient_gen: PatientGen = Depends(get_patient_generator)
):
    if limit <= 0 or limit > 100:
        raise HTTPException(422, "Invalid limit")

    data = []
    for _ in range(limit):
        patient = next(patient_gen.get_patient())
        patient.assign_random_fraction_time()
        data.append(patient.to_dict())

    return {
        "items": data,
        "total": 100_000,
    }


@app.get("/cancers", response_model=PagedResponse[CancerModel])
def get_cancers(offset: int = 0, limit: int = 100):
    data = sorted(
        [cancer.to_dict() for cancer in CANCER_MAP.values()], key=lambda c: c["name"]
    )

    return {
        "items": data[offset : offset + limit],
        "total": len(data),
    }


@app.get("/machines", response_model=PagedResponse)
def get_machines(
    offset: int = 0,
    limit: int = 100,
    machine_pool: MachinePool = Depends(get_machine_pool),
):
    data = sorted(
        [machine.to_dict() for machine in machine_pool.get_all_machines()],
        key=lambda c: c["name"],
    )
    return {
        "items": data[offset : offset + limit],
        "total": len(data),
    }
