from typing import List, TypeVar, Generic

from pydantic import BaseModel, Field
from pydantic.v1.generics import GenericModel

from scheduling.constants import MACHINE_TYPES
from scheduling.diseases import CANCER_MAP


class MakeAppointmentRequest(BaseModel):
    name: str
    cancer_type: str = Field(enum=list(CANCER_MAP.keys()))
    fraction_time: int
    is_urgent: bool = False


class MakeAppointmentResponse(BaseModel):
    machine_name: str = Field(enum=MACHINE_TYPES)
    shift: int


class MachineLoad(BaseModel):
    machine_name: str = Field(enum=MACHINE_TYPES)
    load: float


class GetLoadResponse(BaseModel):
    items: List[MachineLoad]
    average_load: float


class CancerModel(BaseModel):
    name: str
    probability: float
    fraction_times: List[int]
    treatment_time_minutes: int


M = TypeVar("M")


class PagedResponse(BaseModel, Generic[M]):
    items: List[M]
    total: int


class PatientModel(BaseModel):
    name: str
    fraction_time_days: int = Field(
        -1, description="Prescribed fraction time. -1 means that no time was prescribed"
    )
    cancer: CancerModel
