from typing import List

from pydantic import BaseModel, Field

from scheduling.constants import MACHINE_TYPES
from scheduling.diseases import CANCER_MAP


class MakeAppointmentRequest(BaseModel):
    name: str
    cancer_type: str = Field(enum=list(CANCER_MAP.keys()))
    fraction_time: int


class MakeAppointmentResponse(BaseModel):
    machine_name: str = Field(enum=MACHINE_TYPES)
    shift: int


class MachineLoad(BaseModel):
    machine_name: str = Field(enum=MACHINE_TYPES)
    load: float


class GetLoadResponse(BaseModel):
    items: List[MachineLoad]
    average_load: float
